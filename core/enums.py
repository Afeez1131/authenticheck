from django.db import models


class CategoryChoices(models.TextChoices):
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    BEAUTY = 'Beauty'
    FOOD = 'Food'
    HOME_APPLIANCES = 'Home Appliances'
    BOOKS = 'Books'
    SPORTS_OUTDOORS = 'Sports & Outdoors'
    TOYS = 'Toys'
    HEALTH_WELLNESS = 'Health & Wellness'
    FURNITURE = 'Furniture'
    JEWELRY = 'Jewelry'
    AUTOMOTIVE = 'Automotive'
    PET_SUPPLIES = 'Pet Supplies'
    ELECTRICAL_TOOLS = 'Electrical Tools'
    MUSIC_INSTRUMENTS = 'Music Instruments'
    ART_CRAFTS = 'Art & Crafts'
    KITCHEN_APPLIANCES = 'Kitchen Appliances'
    GARDEN_OUTDOOR = 'Garden & Outdoor'
    STATIONERY = 'Stationery'
    TECH_GADGETS = 'Tech Gadgets'
    FITNESS_EQUIPMENT = 'Fitness Equipment'
    PARTY_SUPPLIES = 'Party Supplies'
    SOFTWARE = 'Software'
    CAMERAS_PHOTO = 'Cameras & Photo'
    BABY_PRODUCTS = 'Baby Products'
    HOME_DECOR = 'Home Decor'
    TRAVEL_ACCESSORIES = 'Travel Accessories'
    OFFICE_PRODUCTS = 'Office Products'
    MUSIC_MOVIES = 'Music & Movies'
    OTHER = 'Other'
    
    
class FileTypeChoices(models.TextChoices):
    PNG = 'png'
    SVG = 'svg'