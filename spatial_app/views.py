from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Point, Polygon


class PointAPIView(APIView):
    def get(self, request):
        """Retrieve all points or a specific point using query parameter ?id=<point_id>."""
        try:
            point_id = request.query_params.get('id')

            if point_id:
                point = get_object_or_404(Point, id=point_id)
                response_data = {
                    "id": point.id,
                    "name": point.name,
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "extra_data": point.extra_data
                }
            filters = {}
            for key, value in request.query_params.items():
                if key == 'id':
                    continue
                filters[key] = value

            points = Point.objects.filter(**filters)

            response_data = [
                {
                    "id": p.id, "name": p.name, "latitude": p.latitude, "longitude": p.longitude,
                    "extra_data": p.extra_data
                }
                for p in points
            ]

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new Point with dynamic JSON data."""
        try:
            data = request.data

            name = data.get("name")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            extra_data = data.get("extra_data", {})

            if not name or latitude is None or longitude is None:
                return Response({"error": "Name, latitude, and longitude are required fields."}, status=status.HTTP_400_BAD_REQUEST)

            latitude = float(latitude)
            longitude = float(longitude)

            if Point.objects.filter(latitude=latitude, longitude=longitude).exists():
                return Response({"error": "Point with these coordinates already exists."}, status=status.HTTP_400_BAD_REQUEST)

            point = Point.objects.create(name=name, latitude=latitude, longitude=longitude, extra_data=extra_data)

            return Response({
                "id": point.id, "name": point.name, "latitude": point.latitude, "longitude": point.longitude,
                "extra_data": point.extra_data
            }, status=status.HTTP_201_CREATED)

        except ValueError:
            return Response({"error": "Latitude and Longitude must be numeric values."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update a specific Point using query parameter ?id=<point_id>, allowing dynamic updates."""
        try:
            point_id = request.query_params.get('id')
            if not point_id:
                return Response({"error": "Point ID is required to update."}, status=status.HTTP_400_BAD_REQUEST)

            point = get_object_or_404(Point, id=point_id)
            data = request.data

            point.name = data.get("name", point.name)
            point.latitude = data.get("latitude", point.latitude)
            point.longitude = data.get("longitude", point.longitude)
            point.extra_data.update(data.get("extra_data", {}))
            point.save()

            return Response({
                "id": point.id, "name": point.name, "latitude": point.latitude, "longitude": point.longitude,
                "extra_data": point.extra_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete a specific Point using query parameter ?id=<point_id>."""
        try:
            point_id = request.query_params.get('id')
            if not point_id:
                return Response({"error": "Point ID is required to delete."}, status=status.HTTP_400_BAD_REQUEST)

            point = get_object_or_404(Point, id=point_id)
            point.delete()

            return Response({"message": "Point deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PolygonAPIView(APIView):
    def get(self, request):
        """Retrieve all polygons or a specific polygon using query parameter ?id=<polygon_id>."""
        try:
            polygon_id = request.query_params.get('id')

            if polygon_id:
                polygon = get_object_or_404(Polygon, id=polygon_id)
                response_data = {
                    "id": polygon.id,
                    "name": polygon.name,
                    "coordinates": polygon.coordinates,
                    "extra_data": polygon.extra_data
                }
            filters = {}
            for key, value in request.query_params.items():
                if key == 'id':
                    continue
                filters[key] = value

            polygons = Polygon.objects.filter(**filters)

            response_data = [
                {
                    "id": p.id, "name": p.name, "coordinates": p.coordinates,
                    "extra_data": p.extra_data
                }
                for p in polygons
            ]

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new Polygon with dynamic JSON data."""
        try:
            data = request.data

            name = data.get("name")
            coordinates = data.get("coordinates")

            extra_data = data.get("extra_data", {})

            if not name or not coordinates:
                return Response({"error": "Name and coordinates are required fields."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(coordinates, list) or len(coordinates) < 3:
                return Response({"error": "A polygon must have at least 3 coordinate points."}, status=status.HTTP_400_BAD_REQUEST)

            polygon = Polygon.objects.create(name=name, coordinates=coordinates, extra_data=extra_data)

            return Response({
                "id": polygon.id, "name": polygon.name, "coordinates": polygon.coordinates,
                "extra_data": polygon.extra_data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update a specific Polygon using query parameter ?id=<polygon_id>, allowing dynamic updates."""
        try:
            polygon_id = request.query_params.get('id')
            if not polygon_id:
                return Response({"error": "Polygon ID is required to update."}, status=status.HTTP_400_BAD_REQUEST)

            polygon = get_object_or_404(Polygon, id=polygon_id)
            data = request.data

            polygon.name = data.get("name", polygon.name)
            polygon.coordinates = data.get("coordinates", polygon.coordinates)
            polygon.extra_data.update(data.get("extra_data", {}))
            polygon.save()

            return Response({
                "id": polygon.id, "name": polygon.name, "coordinates": polygon.coordinates,
                "extra_data": polygon.extra_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete a specific Polygon using query parameter ?id=<polygon_id>."""
        try:
            polygon_id = request.query_params.get('id')
            if not polygon_id:
                return Response({"error": "Polygon ID is required to delete."}, status=status.HTTP_400_BAD_REQUEST)

            polygon = get_object_or_404(Polygon, id=polygon_id)
            polygon.delete()

            return Response({"message": "Polygon deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
