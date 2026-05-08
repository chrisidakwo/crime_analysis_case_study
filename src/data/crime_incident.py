class CrimeIncident:
    """
    Represents a single crime incident record from the Chicago Police Department CLEAR system
    """

    # Class Attribute
    VIOLENT_CRIME_TYPES = {
        "HOMICIDE", "BATTERY", "ROBBERY", "SEX OFFENSE", "CRIM SEXUAL ASSAULT", "KIDNAPPING"
    }

    def __init__(self, incident_id, primary_type, incident_date, district, arrest, domestic):
        self.incident_id = incident_id
        self.primary_type = primary_type
        self.incident_date = incident_date
        self.district = district
        self.arrest = arrest
        self.domestic = domestic

    def is_violent(self) -> bool:
        """Return True if the incident is classified as a violent crime."""
        return self.primary_type in self.VIOLENT_CRIME_TYPES

    def is_domestic_violence(self) -> bool:
        """Return True if this is both domestic and a violent crime"""
        return int(self.domestic) == 1 and self.is_violent()

    def was_resolved(self) -> bool:
        """Return True if the incident resulted in an arrest"""
        return int(self.arrest) == 1

    def summary(self):
        """Return a human-readable summary of the incident"""
        arrest_status = "Arrest made" if int(self.arrest) == 1 else "No Arrest made"
        domestic_flag = " [DOMESTIC]" if int(self.domestic) == 1 else ""

        return (
            f"[{self.incident_id}] {self.primary_type}{domestic_flag} - "
            f"District {self.district} | {self.incident_date} | {arrest_status}"
        )


incident = CrimeIncident(
    district="11",
    primary_type="ROBBERY",
    arrest=1,
    incident_date="2022-03-14 08:30:00",
    domestic=0,
    incident_id=10000003,
)

incident_ab = CrimeIncident(
    district="14",
    primary_type="HOMICIDE",
    arrest=1,
    incident_date="2022-03-14 11:17:00",
    domestic=0,
    incident_id=10000893,
)

print("")
print(incident.is_violent())
print(incident.is_domestic_violence())
print(incident.was_resolved())
print(incident.summary())
print("")