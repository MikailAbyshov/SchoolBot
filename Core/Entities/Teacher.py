from dataclasses import dataclass
@dataclass
class Teacher:
    self_id: int
    name: str
    subjects: str # В дальнейшем скорее всего переделаем в subject_id  добавим сущности предметы
    requisites: str
    telegram_tag: str
    discord_tag: str

    @classmethod
    def create(
            cls,
            self_id: int,
            name: str,
            subjects: str,
            requisites: str,
            telegram_tag: str,
            discord_tag: str
    ) -> "Teacher":
        if (self_id is not None) and (self_id < 1):
            raise ValueError("id должен быть >= 1")
        if len(name) > 100:
            raise ValueError("Макс. длина name 100 символов")
        if len(subjects) > 100:
            raise ValueError("Макс. длина subjects 100 символов")
        if len(requisites) > 100:
            raise ValueError("Макс. длина requisites 100 символов")
        if len(telegram_tag) > 100:
            raise ValueError("Макс. длина telegram_tag 100 символов")
        if len(discord_tag) > 100:
            raise ValueError("Макс. длина discord_tag 100 символов")
        return cls(self_id, name, subjects,
                   requisites, telegram_tag, discord_tag)


