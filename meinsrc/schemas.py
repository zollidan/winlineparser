from pydantic import BaseModel, field_validator


class FootballRow(BaseModel):
    date: int

    team_name_1: str
    team_name_2: str

    bookmaker_company_name: str = 'Winline'
    league_name: str

    match_outcome_1: float | str
    match_outcome_2: float | str
    match_outcome_x: float | str

    match_total_m: float | str
    match_total_b: float | str
    match_total_coefficient: float | str

    @classmethod
    @field_validator('match_outcome_1', 'match_outcome_2', 'match_outcome_x', 'match_total_m', 'match_total_b', 'match_total_coefficient')
    def check_data(cls, v):
        if v == '-':
            return v
        return float(v)
