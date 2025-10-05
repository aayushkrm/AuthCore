# This file intentionally minimal - we're using mock data without real models
# In production, you would create actual models here with owner_id fields

# Example of what a real model would look like:
# 
# from django.db import models
# from authentication.models import User
#
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=100)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
