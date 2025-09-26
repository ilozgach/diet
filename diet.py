import collections
import typing

from py_markdown_table.markdown_table import markdown_table

class Macronutrients():
    pfcc = {
        "овсянка": (11.86, 5.08, 58.57, 318.66),
        "молоко 3.2%": (2.8, 3.2, 4.7, 70),
        "шоколад": (8.9, 45, 38, 557.6),
        "суп": (3.8, 2.9, 2.8, 50),
        "яблоко": (0.4, 0, 11.3, 46),
        "курица": (20.8, 8.8, 0.6, 164),
        "рис": (8, 1, 76, 345),
        "помидор": (1, 0.2, 3.7, 20),
        "яйцо": (12.7, 11.5, 0.7, 157),
        "банан": (1.5, 0, 22, 94),
        "крабовый салат": (6.5, 8.1, 9.3, 137.4),
        "ржаной хлеб": (13, 3, 40, 250),
        "творог 9%": (16.7, 9, 1.3, 153),
        "мед": (0.8, 8, 80.3, 324),
        "кешью": (25.7, 54.1, 13.2, 643),
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
            pfcc = Macronutrients.get_pfcc(name, weight)
            total_pfcc = [x + y for x, y in zip(total_pfcc, pfcc)]
        return total_pfcc

####################################################################################################
# BREAKFAST ########################################################################################
####################################################################################################

breakfast_08_00 = Meal("завтрак 08:00", [("овсянка", 35), ("молоко 3.2%", 270), ("шоколад", 25)])
# breakfast_2 = Meal("завтрак 2", [("суп", 400), ("яблоко", 150)])

####################################################################################################
# LUNCH ############################################################################################
####################################################################################################

# lunch_1 = Meal("обед", [("курица", 200), ("рис", 30), ("помидор", 200)])
lunch_12_30 = Meal("обед 12:30", [("суп", 400), ("яблоко", 150)])

####################################################################################################
# SNACK ############################################################################################
####################################################################################################

# snack_1 = Meal("полдник", [("яйцо", 50), ("банан", 250)])
snack_15_00 = Meal("полдник 15:00", [("курица", 200), ("рис", 30), ("помидор", 200)])

####################################################################################################
# DINNER ###########################################################################################
####################################################################################################

dinner_19_00 = Meal("ужин 19:00", [("крабовый салат", 200), ("ржаной хлеб", 50)])
dinner_21_00 = Meal("ужин 21:00", [("творог 9%", 90), ("мед", 20), ("кешью", 10)])

####################################################################################################
# MAIN #############################################################################################
####################################################################################################

if __name__ == "__main__":
    meals = [breakfast_08_00, lunch_12_30, snack_15_00, dinner_19_00, dinner_21_00]

    total_pfcc = [0, 0, 0, 0]
    for meal in meals:
        pfcc = meal.get_pfcc()
        total_pfcc = [x + y for x, y in zip(total_pfcc, pfcc)]

    with open("README.md", "w") as f:
        for meal in meals:
            f.write(f"**{meal.name}**\n\n")

            table_data = []
            for item_name, item_weight in meal.content:
                protein, fat, carbohydrate, calorie = Macronutrients.get_pfcc(item_name, item_weight)

                table_data.append({
                    "продукт": item_name,
                    "вес": item_weight,
                    "белки": f"{protein:.2f}",
                    "жиры": f"{fat:.2f}",
                    "углеводы": f"{carbohydrate:.2f}",
                    "ккал": f"{calorie:.2f}",
                })

            pfcc = meal.get_pfcc()
            table_data.append({
                "продукт": "",
                "вес": "",
                "белки": f"{pfcc[0]:.2f} - {pfcc[0] / total_pfcc[0] * 100:.2f}%",
                "жиры": f"{pfcc[1]:.2f} - {pfcc[1] / total_pfcc[1] * 100:.2f}%",
                "углеводы": f"{pfcc[2]:.2f} - {pfcc[2] / total_pfcc[2] * 100:.2f}%",
                "ккал": f"{pfcc[3]:.2f} - {pfcc[3] / total_pfcc[3] * 100:.2f}%",
            })

            markdown = markdown_table(table_data).get_markdown()
            f.write(markdown + "\n")
        
        f.write(f"**выход**\n\n")
        macros_total_weight = total_pfcc[0] + total_pfcc[1] + total_pfcc[2]
        table_data = [{
            "белки": f"{total_pfcc[0]:.2f} - {total_pfcc[0] / macros_total_weight * 100:.2f}%",
            "жиры": f"{total_pfcc[1]:.2f} - {total_pfcc[1] / macros_total_weight * 100:.2f}%",
            "углеводы": f"{total_pfcc[2]:.2f} - {total_pfcc[2] / macros_total_weight * 100:.2f}%",
            "ккал": f"{total_pfcc[3]:.2f}",
        }]

        markdown = markdown_table(table_data).get_markdown()
        f.write(markdown + "\n")
