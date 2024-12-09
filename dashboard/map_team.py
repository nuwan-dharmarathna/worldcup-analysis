def get_team_name(team):
    """Return the country name."""
    country_map = {
        'AFG': 'Afghanistan',
        'AUS': 'Australia',
        'BAN': 'Bangladesh',
        'BER': 'Bermuda',
        'CAN': 'Canada',
        'EAF': 'EAF',
        'ENG': 'England',
        'IND': 'India',
        'IRE': 'Ireland',
        'KENYA': 'Kenya',
        'NAM': 'Namibia',
        'NED': 'Netherlands',
        'NZ': 'NZ',
        'PAK': 'Pakistan',
        'SA': 'SA',
        'SCOT': 'Scotland',
        'SL': 'SL',
        'UAE': 'UAE',
        'WI': 'WI',
        'ZIM': 'Zimbabwe'
    }
    return country_map.get(team)