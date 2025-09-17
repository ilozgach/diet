import collections
import typing

from py_markdown_table.markdown_table import markdown_table

class Macronutrients():
    pfcc = {
        "овсянка": (11.86, 5.08, 58.57, 318.66),
        "молоко 3.2%": (3.2, 3.0, 4.7, 60),
        "шоколад": (8.9, 45, 38, 557.6)
    }

    @staticmethod
    def get_pfcc(name: str, weight: int | None) -> list[float] | None:
        if name not in Macronutrients.pfcc:
            return None
        if weight is None:
            return Macronutrients.pfcc[name]
        return [x / 100.0 * weight for x in Macronutrients.pfcc[name]]


class Meal():
    def __init__(self, name: str, content: list[typing.Tuple]) -> None:
        self.name = name
        self.content = content
    
    def get_pfcc(self):
        total_pfcc = [0, 0, 0, 0]
        for name, weight in self.content:
            pfcc = Macronutrients.get(name, weight)
            total_pfcc = [x + y for x, y in zip(total_pfcc, pfcc)]
        return total_pfcc

####################################################################################################
# BREAKFAST ########################################################################################
####################################################################################################

breakfast_1 = Meal("завтрак", [("овсянка", 35), ("молоко 3.2%", 270), ("шоколад", 25)])

####################################################################################################
# LUNCH ############################################################################################
####################################################################################################



####################################################################################################
# DINNER ###########################################################################################
####################################################################################################



####################################################################################################
# MAIN #############################################################################################
####################################################################################################

if __name__ == "__main__":
    meals = [breakfast_1]
    nutrutions_per_meal = {}
    total_nutritions = [0, 0, 0, 0]
    
    with open("README.md", "w") as f:
        for meal in meals:
            f.write(f"**{meal.name}**\n\n")

            table_data = []
            for item_name, item_weight in meal.content:
                protein, fat, carbohydrate, calorie = Macronutrients.get_pfcc(item_name, item_weight)

                table_data.append({
                    "продукт": item_name,
                    "вес": item_weight,
                    "белки": protein,
                    "жиры": fat,
                    "углеводы": carbohydrate,
                    "ккал": calorie,
                })

            markdown = markdown_table(table_data).get_markdown()
            f.write(markdown + "\n")
    