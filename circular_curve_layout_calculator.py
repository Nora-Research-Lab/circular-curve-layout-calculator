import math

DEFAULT_INTERVAL_METERS = 10.0
DEFAULT_INTERVAL_FEET = 25.0

def parse_station_error(station_str):
    """Parse station string 'XX+YY.ZZ' to float. Returns float or raises ValueError."""
    station_str = station_str.strip()
    if station_str.count('+') != 1:
        raise ValueError("Station format must be 'XX+YY.ZZ' (e.g., 12+45.67)")
    parts = station_str.split('+')
    try:
        hundreds = int(parts[0])
        decimal_part = float(parts[1])
    except (ValueError, IndexError):
        raise ValueError("Station format must be 'XX+YY.ZZ' with numeric values")
    return hundreds * 100 + decimal_part

def format_station(value):
    """Convert float to station string 'XX+YY.ZZ'."""
    if value < 0:
        raise ValueError("Station cannot be negative")
    hundreds = int(value // 100)
    remainder = value - hundreds * 100
    return f"{hundreds}+{remainder:05.2f}"

def compute_curve(delta_deg, radius, unit, pi_station_str, interval):
    """
    Compute circular curve layout.
    Returns dict with keys: delta_deg, radius, unit, T, L, C, E, M,
    pc_station, pt_station, layout (list of dicts with keys: station, deflection_deg, chord_distance).
    """
    # Input validation
    if not (0 < delta_deg < 180):
        raise ValueError("Δ must be between 0 and 180 degrees")
    if radius <= 0:
        raise ValueError("Radius must be positive")
    if interval <= 0:
        raise ValueError("Interval must be positive")
    
    delta_rad = math.radians(delta_deg)
    half_delta = delta_rad / 2
    
    T = radius * math.tan(half_delta)
    L = radius * delta_rad
    C = 2 * radius * math.sin(half_delta)
    E = radius * (1 / math.cos(half_delta) - 1)
    M = radius * (1 - math.cos(half_delta))
    
    pi_station = parse_station_error(pi_station_str)
    pc_station = pi_station - T
    pt_station = pc_station + L
    
    # Generate layout stations
    layout = []
    # Add PC
    layout.append({
        "station": format_station(pc_station),
        "deflection_deg": 0.0,
        "chord_distance": 0.0
    })
    # Intermediate points
    current = pc_station + interval
    while current < pt_station - 1e-9:  # tolerance to avoid floating point issues
        arc_len = current - pc_station
        central_angle_rad = arc_len / radius
        half_central = central_angle_rad / 2
        deflection_deg = math.degrees(half_central)
        chord = 2 * radius * math.sin(half_central)
        layout.append({
            "station": format_station(current),
            "deflection_deg": deflection_deg,
            "chord_distance": chord
        })
        current += interval
    # Add PT
    arc_len = pt_station - pc_station
    central_angle_rad = arc_len / radius
    half_central = central_angle_rad / 2
    deflection_deg = math.degrees(half_central)
    chord = 2 * radius * math.sin(half_central)
    layout.append({
        "station": format_station(pt_station),
        "deflection_deg": deflection_deg,
        "chord_distance": chord
    })
    
    return {
        "delta_deg": delta_deg,
        "radius": radius,
        "unit": unit,
        "T": T,
        "L": L,
        "C": C,
        "E": E,
        "M": M,
        "pc_station": format_station(pc_station),
        "pt_station": format_station(pt_station),
        "layout": layout
    }
