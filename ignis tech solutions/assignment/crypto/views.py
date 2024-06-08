from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin_data
import logging

logger = logging.getLogger(__name__)

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        job_ids = []
        for coin in coins:
            result = scrape_coin_data.delay(coin)
            job_ids.append(result.id)
        return Response({'job_ids': job_ids}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        result = AsyncResult(job_id)
        logger.info(f"Checking status for job_id: {job_id}")
        if result.state == 'PENDING':
            logger.info(f"Job {job_id} is pending")
            return Response({"status": "pending"}, status=status.HTTP_200_OK)
        elif result.state == 'FAILURE':
            logger.error(f"Job {job_id} failed")
            return Response({"status": "failed", "error": str(result.result)}, status=status.HTTP_200_OK)
        elif result.state == 'SUCCESS':
            logger.info(f"Job {job_id} succeeded")
            return Response(result.result, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Job {job_id} is in state {result.state}")
            return Response({"status": result.state}, status=status.HTTP_200_OK)
