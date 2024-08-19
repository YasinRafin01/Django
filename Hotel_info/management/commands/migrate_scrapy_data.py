import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from Hotel_info.models import Property, PropertyImage, Location
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL,SCRAPY_IMAGE_DIR

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(String, unique=True)
    hotel_name = Column(String)
    hotel_url = Column(String)
    hotel_location = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    image_url = Column(String)  # This contains the filename from Scrapy project
    price = Column(Float)
    city = Column(String)
    section = Column(String)

# SCRAPY_IMAGE_DIR = '/home/w3e100/Downloads/Scrapy_Project-main/trip_scraper/images'

def copy_image(src_filename, dst_path):
    """
    Copy image from Scrapy project to Django media directory
    """
    try:
        src_path = os.path.join(SCRAPY_IMAGE_DIR, src_filename)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        return True
    except Exception as e:
        print(f"Error copying image: {e}")
        return False

class Command(BaseCommand):
    help = 'Migrate data from Scrapy project database to Django'

    def handle(self, *args, **kwargs):
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        hotels = session.query(Hotel).all()

        for hotel in hotels:
            property, created = Property.objects.update_or_create(
                property_id=hotel.hotel_id,
                defaults={
                    'title': hotel.hotel_name,
                    'description': hotel.hotel_url,
                }
            )

            if hotel.hotel_location:
                location, _ = Location.objects.get_or_create(
                    name=hotel.hotel_location,
                    defaults={
                        'type': 'city',
                        'latitude': hotel.latitude if hotel.latitude is not None else 0,
                        'longitude': hotel.longitude if hotel.longitude is not None else 0,
                    }
                )
                property.locations.add(location)

            # Handle image
            if hotel.image_url:
                # Construct paths
                file_name = os.path.basename(hotel.image_url)
                hotel_specific_dir = os.path.join('property_images', hotel.hotel_id)
                django_image_path = os.path.join(settings.MEDIA_ROOT, hotel_specific_dir, file_name)

                # Copy image from Scrapy project to Django media directory
                if copy_image(file_name, django_image_path):
                    # Create PropertyImage object with the new path
                    relative_path = os.path.join(hotel_specific_dir, file_name)
                    property_image, created = PropertyImage.objects.get_or_create(
                        property=property,
                        defaults={'image': relative_path}
                    )
                    if not created:
                        property_image.image = relative_path
                        property_image.save()

            self.stdout.write(self.style.SUCCESS(f'Migrated hotel: {hotel.hotel_name}'))

        session.close()
        self.stdout.write(self.style.SUCCESS('Successfully migrated data from Scrapy to Django'))
