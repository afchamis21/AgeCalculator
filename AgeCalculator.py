from datetime import date


class AgeCalculator:
    def __init__(self):
        self.target_date: str = ''
        self.__months_with_30_days = [1, 3, 5, 7, 8, 10, 12]
        self.__months_with_31_days = [4, 6, 9, 11]

    @staticmethod
    def __is_leap_year(year: int) -> bool:
        if year % 4 == 0 and year % 100 != 0:
            return True

        if year % 400 == 0:
            return True

        return False

    @staticmethod
    def __get_formatted_date(date_to_format) -> list[int]:
        return [*map(int, date_to_format.split('/'))]

    def __is_valid_date(self, birth_date: str) -> bool:
        try:
            formatted_date = self.__get_formatted_date(birth_date)
            day, month, year = formatted_date

            current_year = int(date.today().strftime("%Y"))
            if year > current_year:
                print('O ano não pode ser maior que o atual')
                return False

            if month < 1 or month > 12:
                print('Mês inválido')
                return False

            if month in self.__months_with_30_days and (day < 1 or day > 30):
                print('Dia inválido, esse mês possui 30 dias')
                return False

            if month in self.__months_with_31_days and (day < 1 or day > 31):
                print('Dia inválido, esse mês possui 31 dias')
                return False

            if month == 2 and self.__is_leap_year(year) and (day < 1 or day > 29):
                print('Dia inválido, em anos bissextos, Fevereiro possui 29 dias')
                return False

            if month == 2 and not self.__is_leap_year(year) and (day < 1 or day > 28):
                print('Dia inválido, Fevereiro possui 28 dias')
                return False

            return True

        except ValueError:
            print('Por favor, digite a data no formato numérico DD/MM/YYYY\n Ex: -> 21/05/2001 \n')
            return False

    def __convert_year_range_to_days(self, target_year: int) -> int:
        days_per_year = [366 if self.__is_leap_year(year) else 365 for year in range(1, target_year)]
        amount_of_days = sum(days_per_year)
        return amount_of_days

    def __convert_month_range_to_days(self, target_month: int, is_leap_year: bool) -> int:
        total_days = 0
        for month in range(1, target_month):
            if month in self.__months_with_31_days:
                total_days += 31
            elif month in self.__months_with_30_days:
                total_days += 30
            elif is_leap_year and month == 2:
                total_days += 29
            elif month == 2:
                total_days += 28

        return total_days

    def __convert_date_to_days_amount(self, target_date: str) -> int:
        formatted_date = self.__get_formatted_date(target_date)
        target_day, target_month, target_year = formatted_date
        target_month_in_days = self.__convert_month_range_to_days(target_month, self.__is_leap_year(target_year))
        target_year_in_days = self.__convert_year_range_to_days(target_year)
        total_days_until_today = target_day + target_month_in_days + target_year_in_days

        return total_days_until_today

    def __convert_days_to_complete_date(self, amount_of_days: int, starting_year: int) -> str:
        present_year = int(date.today().strftime("%Y"))
        years = 0
        for year in range(starting_year, present_year):
            if self.__is_leap_year(year):
                if amount_of_days < 366:
                    break
                amount_of_days -= 366
            else:
                if amount_of_days < 365:
                    break
                amount_of_days -= 365
            years += 1

        months_counted = 0
        is_counting_months = True
        while is_counting_months:
            if months_counted + 1 in self.__months_with_30_days:
                if amount_of_days < 30:
                    is_counting_months = False
                    continue
                else:
                    amount_of_days -= 30

            elif months_counted + 1 in self.__months_with_31_days:
                if amount_of_days < 31:
                    is_counting_months = False
                    continue
                else:
                    amount_of_days -= 31

            elif months_counted + 1 == 2 and self.__is_leap_year(present_year):
                if amount_of_days < 29:
                    is_counting_months = False
                    continue
                else:
                    amount_of_days -= 29

            elif months_counted + 1 == 2:
                if amount_of_days < 28:
                    is_counting_months = False
                    continue
                else:
                    amount_of_days -= 28

            months_counted += 1
        return f"{years} anos, {months_counted} meses e {amount_of_days} dias"

    def get_date_input(self) -> None:
        while True:
            target_date = input('Digite a data alvo no formato DD/MM/YYYY: ')
            if self.__is_valid_date(target_date):
                self.target_date = target_date
                break

    def calculate_age_from_birth_date(self) -> int:
        today = date.today().strftime("%d/%m/%Y")
        total_days_until_today = self.__convert_date_to_days_amount(today) - 1
        total_days_until_target_date = self.__convert_date_to_days_amount(self.target_date)
        days_bewteen_target_and_today = total_days_until_today - total_days_until_target_date

        age = days_bewteen_target_and_today // 365
        age_with_months_and_days = self.__convert_days_to_complete_date(days_bewteen_target_and_today, int(self.target_date.split('/')[-1]))
        age_and_days = f"{age} anos e {days_bewteen_target_and_today % 365} dias"

        print(f"A idade calculada em anos é :"
              f"\n - {age} anos,"
              f"\n - {age_with_months_and_days},"
              f"\n - {age_and_days},"
              f"\n - {days_bewteen_target_and_today} dias")

    def start(self):
        self.get_date_input()
        self.calculate_age_from_birth_date()
