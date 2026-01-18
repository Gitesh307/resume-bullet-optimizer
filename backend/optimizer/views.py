from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OptimizeRequestSerializer, OptimizeResponseSerializer
from .nlp import rewrite_bullet

class HealthView(APIView):
    def get(self, request):
        return Response({"ok": True})

class OptimizeBulletView(APIView):
    def post(self, request):
        req = OptimizeRequestSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)

        bullet = req.validated_data["bullet"]
        jd = req.validated_data["job_description"]

        result = rewrite_bullet(bullet, jd)

        resp = OptimizeResponseSerializer(data=result)
        resp.is_valid(raise_exception=True)
        return Response(resp.data, status=status.HTTP_200_OK)
