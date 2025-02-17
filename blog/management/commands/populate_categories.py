from blog.models import Category
from django.core.management.base import BaseCommand
from typing  import Any

class Command(BaseCommand):
    help ='this commands inserts post data'

    def handle(self, *args:Any, **options:Any):   
        # Delete the existing data to add the slug feild 
        Category.objects.all().delete() 
        Categories =['Sports','Technology','Science','Art']
  
        for  category_name in Categories:
            Category.objects.create(name = category_name)            

        self.stdout.write(self.style.SUCCESS('completed inserting Data!'))