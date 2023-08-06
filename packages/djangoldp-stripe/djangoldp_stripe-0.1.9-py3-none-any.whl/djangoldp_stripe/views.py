from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from djangoldp.views import NoCSRFAuthentication
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes 
from djstripe.models.core import Price
import stripe

from djangoldp_stripe.permissions import user_has_any_active_subscription

STRIPE_LIVE_SECRET_KEY = settings.STRIPE_LIVE_SECRET_KEY
STRIPE_LIVE_MODE = settings.STRIPE_LIVE_MODE
STRIPE_TEST_SECRET_KEY = settings.STRIPE_TEST_SECRET_KEY

stripe.api_key = STRIPE_LIVE_SECRET_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_SECRET_KEY


class SuccessPageView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def get(self, request):
        return render(request, 'success.html')


class CancelledPageView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def get(self, request):
        return render(request, 'cancel.html')


class CheckoutSessionView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def get(self, request):
        # lookup_key must be passed in the requesting form
        lookup_key = request.GET.get('lookup_key', None)

        if lookup_key is None:
            raise ValidationError('lookup_key is required')

        price = get_object_or_404(Price, lookup_key=lookup_key)

        return render(request, 'checkout.html', context={'product': price.product, 'price': price, 'unit_amount': price.unit_amount * 0.01})

    def post(self, request):
        # lookup_key must be passed in the requesting form
        lookup_key = request.data.get('lookup_key', None)

        if lookup_key is None:
            raise ValidationError('lookup_key is required')

        price = get_object_or_404(Price, lookup_key=lookup_key)
        host_url = settings.SITE_URL

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=host_url + '/checkout-session/success/',
            cancel_url=host_url + '/checkout-session/cancel/',
        )
        return redirect(checkout_session.url)


class UserHasValidSubscriptionView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        '''overriden dispatch method to append some custom headers'''
        response = super(UserHasValidSubscriptionView, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.META.get('HTTP_ORIGIN')
        response["Access-Control-Allow-Methods"] = "GET"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

    @permission_classes([IsAuthenticated])
    def get(self, request):
        if user_has_any_active_subscription(request.user):
            return Response(True, status=status.HTTP_200_OK)
        
        redirect_url = getattr(settings, 'REDIRECT_URL_NO_SUBSCRIPTION', None)
        if redirect_url is not None:
            return redirect(redirect_url)
        
        return Response(False, status=status.HTTP_200_OK)
