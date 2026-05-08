class CrimeIncident:
    """
    Represents a single crime incident record from the Chicago Police Department CLEAR system.

    Each instance holds the data for one specific incident and provides methods
    to interpret and describe that incident in a consistent way.
    """

    # Class Attribute
    VIOLENT_CRIME_TYPES = {
        "HOMICIDE", "BATTERY", "ROBBERY", "SEX OFFENSE", "CRIM SEXUAL ASSAULT", "KIDNAPPING"
    }

    PROPERTY_CRIME_TYPES = {
        "THEFT", "BURGLARY", "CRIMINAL DAMAGE", "CRIMINAL TRESPASS", "ARSON", "MOTOR VEHICLE THEFT"
    }

    def __init__(self, incident_id, primary_type, incident_date, district, arrest, domestic):
        """
        Initialize a CrimeIncident object with the date for one incident
        """
        self.incident_id = incident_id
        self.primary_type = primary_type
        self.incident_date = incident_date
        self.district = district
        self.arrest = arrest
        self.domestic = domestic

    def is_violent(self) -> bool:
        """
        Return True if the incident is classified as a violent crime.
        """
        return self.primary_type in self.VIOLENT_CRIME_TYPES

    def is_property_crime(self):
        """
        Return True if this incident is classified as a property crime

        Returns:
             bool: True if primary_type is in PROPERTY_CRIME_TYPES

        Example:
            incident = CrimeIncident(..., primary_type="THEFT", ...)
            incident.is_property_crime() # True
        """
        return self.primary_type in self.PROPERTY_CRIME_TYPES

    def is_domestic_violence(self) -> bool:
        """
        Return True if this is both domestic and a violent crime
        """
        return int(self.domestic) == 1 and self.is_violent()

    def was_resolved(self) -> bool:
        """
        Return True if the incident resulted in an arrest

        Returns:
            bool: True if arrest == 1 (or True)
        """
        return int(self.arrest) == 1

    def crime_category(self):
        """
        Return the broad category this incident falls into

        Returns:
             str: One of "Violent", "Property", or "Other"
        """
        if self.is_violent():
            return "Violent"
        elif self.is_property_crime():
            return "Property"
        else:
            return "Other"

    def summary(self) -> str:
        """
        Return a human-readable summary of the incident

        Returns:
            str: A formatted description of the incident
        """
        arrest_status = "Arrest made" if int(self.arrest) == 1 else "No Arrest made"
        domestic_flag = " [DOMESTIC]" if int(self.domestic) == 1 else ""

        return (
            f"[{self.incident_id}] - {self.primary_type.title()}{domestic_flag} in "
            f"District {self.district} | {self.incident_date} | {arrest_status}"
        )

    def __repr__(self) -> str:
        """
        Return a concise, unambiguous representation of this object.
        Such that the object can be recreated from the return value.

        This is what Python shows when you print the object directly,
        place it in a `repr()` function, or inspect it in a list.

        Returns:
             str: A developer-friendly string representation of this object
        """
        return (
            f"CrimeIncident("
            f"incident_id='{self.incident_id}',"
            f"primary_type='{self.primary_type}',"
            f"incident_date='{self.incident_date}',"
            f"district='{self.district}',"
            f"arrest={self.arrest},"
            f"domestic={self.domestic})"
        )

    def __str__(self) -> str:
        """
        Return a description of the incident, such that it can be easily understood.

        Returns:
             str: A human-readable string representation of this object
        """
        return self.summary()
