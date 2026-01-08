class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # generar ID devuelve el ID generado
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        if not isinstance(member, dict):
            return None

        first_name = member.get("first_name")
        age = member.get("age")
        lucky_numbers = member.get("lucky_numbers")

        if not isinstance(first_name, str) or not first_name.strip():
            return None
        if not isinstance(age, int) or age <= 0:
            return None
        if not isinstance(lucky_numbers, list) or not all(isinstance(n, int) for n in lucky_numbers):
            return None

        new_member = {
            "id": self._generate_id(),
            "first_name": first_name.strip(),
            "last_name": self.last_name,
            "age": age,
            "lucky_numbers": lucky_numbers
        }

        self._members.append(new_member)
        return new_member

    def delete_member(self, id):
        for i, m in enumerate(self._members):
            if m.get("id") == id:
                self._members.pop(i)
                return True
        return False

    def get_member(self, id):
        for m in self._members:
            if m.get("id") == id:
                return m
        return None

    
    def get_all_members(self, id=None):
        return self._members
