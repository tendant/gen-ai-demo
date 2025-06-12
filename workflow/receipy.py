from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, EmailStr

from pydantic_ai import Agent, format_as_xml
from pydantic_ai.messages import ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from rich.prompt import Prompt
import asyncio
import os
import logfire


@dataclass
class RecipeState:
    available_ingredients: list[str]  | None = None
    dietary_restrictions: str = ""

# Flow: Ingredients → AI Recipe → Cooking Guide


IngredietGenerator = Agent(
    'claude-sonnet-4-20250514',
    output_type=list[str],
    system_prompt='generagte a list of ingredients  that are in the fridge',
)

@dataclass
class GetIngredients(BaseNode[RecipeState]):

    async def run(self, ctx: GraphRunContext[RecipeState]) -> GetPreferences:
        possible_ingredients = await IngredietGenerator.run(user_prompt="give me a list of ingredients that are in the fridge")
        print(possible_ingredients.output)
        ctx.state.available_ingredients = possible_ingredients.output
        return GetPreferences()



@dataclass
class GetPreferences(BaseNode[RecipeState]):
    async def run(self, ctx: GraphRunContext[RecipeState]) -> AIRecipeFinder:
        restriction = Prompt.ask('what is your restriction')
        ctx.state.dietary_restrictions = restriction

        return AIRecipeFinder()


ReceipeGenerater = Agent(
        'claude-sonnet-4-20250514',
        output_type=str,
        system_prompt='generate a recipe based on the ingredients and dietary restrictions',
        )





@dataclass
class AIRecipeFinder(BaseNode[RecipeState]):
    feedback: str | None = None



    async def run(self, ctx: GraphRunContext[RecipeState]) -> FeedBack:
        # combine ingredients and dietary restrictions
        ingredients_text = ', '.join(ctx.state.available_ingredients) if ctx.state.available_ingredients else "no specific ingredients"

        user_prompts = f"Generate a recipe using the following ingredients: {ingredients_text}. " \
           f"Consider the dietary restrictions: {ctx.state.dietary_restrictions}."

        receipt = await ReceipeGenerater.run(user_prompt=user_prompts)
        return FeedBack(receipt.output)





@dataclass
class FeedBack(BaseNode[RecipeState, None, str]):
    Receipt: str

    async def run(self, ctx: GraphRunContext[RecipeState]) -> AIRecipeFinder | End[str]:
        print(f"Recipe: {self.Receipt}")
        fd = Prompt.ask('do you like the recipe?')
        if fd.lower() == 'yes':
            print(f"Here is your recipe: {self.Receipt}")
            return End(self.Receipt)
        else :
            print("Let's try again!")
            feedback = "Let\'s try again!"+ self.Receipt +  " is not good"
            return AIRecipeFinder(feedback)  # Return to recipe finder with feedback


receipt_graph = Graph(
        nodes = [GetIngredients, GetPreferences, AIRecipeFinder, FeedBack],
        )

async def main():
# Configure logfire with token from environment
    logfire_token = os.getenv("LOGFIRE_TOKEN")
    logfire.configure(token=logfire_token)
    logfire.instrument_pydantic_ai()

    receipt_graph.mermaid_save('./workflow/image.png')

    state = RecipeState()

    async with receipt_graph.iter(GetIngredients(), state=state) as run:
        async for node in run:
            print('Node:', node)
    print(run.result)  # Print the final recipe or feedback

if __name__ == '__main__':
    asyncio.run(main())

