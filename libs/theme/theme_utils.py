from typing import List
from enum import Enum

PRIMARY_COLORS: List[str] = ["Red" , "Pink" , "Purple" , "DeepPurple" , "Indigo" , "Blue" ,
    "LightBlue" , "Cyan" , "Teal" , "Green" , "LightGreen" , "Lime" , "Yellow" ,
    "Amber" , "Orange" , "DeepOrange" , "Brown" , "Gray" , "BlueGray"]

ThemeMode: Enum = Enum("ThemeMode", ["Light", "Dark"])
