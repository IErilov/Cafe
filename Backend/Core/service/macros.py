class macros:
    @staticmethod
    def calc_man(m:int, h:int, yo:int)-> int:
        macros = (10*m)+(6.25*h)-(5*yo)+5
        return macros

    @staticmethod
    def calc_girl(m:int, h:int, yo:int)-> int:
        macros = (10*m)+(6.25*h)-(5*yo)-161
        return macros

    @staticmethod
    def activity(active:str) -> float:
        active_check = {
            "low" : 1.2,
            "minimal" : 1.375,
            "midle" : 1.55,
            "high" : 1.725,
            "highest" : 1.9
        }
        return active_check.get(active.lower(), 1.2)

    @classmethod
    def full_macros(cls,
                    gender:str, 
                    m:int,  # massa
                    h:int,  # visota
                    yo:int, 
                    up:bool
                    ):
        if gender.lower() in ["man"]:
            calories = cls.calc_man(m,h,yo)
        elif gender.lower() in ["girl"]:
            calories = cls.calc_girl(m,h,yo)
        else:
            return f"пол {gender.lower()} не найден"

        calories = round(calories * cls.activity())

        if up is True:
            calories = round(calories * 1.15)
        elif up is False:
            calories = round(calories * 0.85)
        else:
            pass

        proteins = round((calories * 0.3) / 4)
        fats = round((calories * 0.3) / 9)
        carbs = round((calories * 0.4) / 4)

        return {
            "calories" : calories,
            "proteins" : proteins,
            "fats" : fats,
            "carbs" : carbs
        }