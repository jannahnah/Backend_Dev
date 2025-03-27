from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact

#class HelloWorld(APIView):
    #def get(self, request):
        #return Response({"message": "Heyow, Ada!"}, status=status.HTTP_200_OK)

class Students(APIView):
    def get(self, request):
        # Define a dictionary with student profiles
        students = {
            1: {
                "student_id": "12345",
                "name": "Walice Johnson",
                "program": "Tourism",
                "year_level": "Sophomore"
            },
            2: {
                "student_id": "S23456",
                "name": "Jane Dow",
                "program": "Environmental Science",
                "year_level": "Junior"
            },
            3: {
                "student_id": "S34567",
                "name": "Red Brown",
                "program": "Business Administration",
                "year_level": "Senior"
            },
            4: {
                "student_id": "S45678",
                "name": "Diana Green",
                "program": "Electrical Engineering",
                "year_level": "Freshman"
            }
        }

        # Return the student dictionary as a response
        return Response(students, status=status.HTTP_200_OK)

class ContactListView(APIView):
    #class helper
    def create_contact(self, data):
        """Helper function to create a Contact object from data."""
        return Contact(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', '')
        )
    
    def post(self, request, *args, **kwargs):
        data = request.data  # Can be a single dict or a list of dicts
        
        if isinstance(data, dict):  # Single entry
            contact = self.create_contact(data)
            contact.save()
            return Response({"message": "Contact added successfully!", "id": contact.id}, status=status.HTTP_201_CREATED)

        elif isinstance(data, list):  # Bulk upload
            contacts = [self.create_contact(item) for item in data]
            Contact.objects.bulk_create(contacts)  # Efficient bulk insert
            return Response({"message": f"{len(contacts)} contacts added successfully!"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, contact_id=None,  *args, **kwargs):
        
        
        if contact_id:  # If contact_id is provided, get the specific contact
            try:
                contact = Contact.objects.get(id=contact_id)
                contact_data = {
                    'id': contact.id,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'email': contact.email,
                    'phone_number': contact.phone_number,
                    'address': contact.address,
                    'created_at': contact.created_at,
                    'updated_at': contact.updated_at,
                }
                return Response({'contact': contact_data})
            except Contact.DoesNotExist:
                return Response({'message': '404'}, status=status.HTTP_404_NOT_FOUND)

         # Get all contacts from the database
        contacts = Contact.objects.all()

        # Manually build the contact data as a list of dictionaries
        contact_data = []
        for contact in contacts:
            contact_data.append({
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone_number': contact.phone_number,
                'address': contact.address,
                'created_at': contact.created_at,
                'updated_at': contact.updated_at,
            })

        # Return the data as a JSON response using DRF's Response
        return Response({'contacts': contact_data})


class ContactUpdateDetailView(APIView):
    # Helper method to get a contact object by ID
    def get_object(self, contact_id):
        try:
            return Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            raise Http404
  
    # DELETE: Delete a contact by ID
    def delete(self, request, contact_id, *args, **kwargs):
        contact = self.get_object(contact_id)
        contact.delete()
        return Response({"message": "Data successfully deleted"}, status=status.HTTP_200_OK)

    # PUT/PATCH: Update a contact by ID
    def put(self, request, contact_id, *args, **kwargs):
        contact = self.get_object(contact_id)
        data = request.data
        
        # Update the contact fields if provided
        contact.first_name = data.get('first_name', contact.first_name)
        contact.last_name = data.get('last_name', contact.last_name)
        contact.email = data.get('email', contact.email)
        contact.phone_number = data.get('phone_number', contact.phone_number)
        contact.address = data.get('address', contact.address)
        contact.save()

        return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)