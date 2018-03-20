from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from web_api import models

class Dpu(View):
    def post(self, request, id):
        timestamp = request.POST.get('timestamp')
        direction = request.POST.get('direction')

        if not all([timestamp, direction]):
            return JsonResponse(
                {'error': 'timestamp and direction fields are required'},
                status=400
            )

        try:
            direction = int(direction)
            assert direction in [-1, 1]
        except:
            return JsonResponse(
                {'error': 'direction must be an integer (-1 or 1)'},
                status=400
            )

        # Get the spaces on either side of this DPU's doorway and update their count
        entering_to = get_object_or_404(models.Space, doorway_entering_to__dpu=id)
        exiting_to = get_object_or_404(models.Space, doorway_exiting_to__dpu=id)

        try:
            self._update_occupancy(entering_to, direction, timestamp)
            self._update_occupancy(exiting_to, direction * -1, timestamp)
        except IntegrityError:
            # This record exists, return 409 CONFLICT
            return HttpResponse(status=409)

        # Return an empty 201 CREATED on success
        return HttpResponse(status=201)

    def _update_occupancy(self, space, direction, timestamp):
        with transaction.atomic():
            try:
                latest_occupancy = models.Occupancy.objects.select_for_update() \
                    .filter(space=space).latest('timestamp')
                new_count = max([0, latest_occupancy.count+direction])
            except models.Occupancy.DoesNotExist:
                # This will be the first record for this space
                new_count = max([0, direction])

            models.Occupancy.objects.create(
                space=space,
                timestamp=timestamp,
                count=new_count
            )

class SpaceCount(View):
    def get(self, request, id):
        timestamp = request.GET.get('timestamp')
        try:
            record = models.Occupancy.objects.filter(space=id)
            if timestamp:
                record = record.filter(timestamp__lte=timestamp)
            count = record.latest('timestamp').count
        except models.Occupancy.DoesNotExist:
            count = 0

        return JsonResponse({'space_id': id, 'count': count})
