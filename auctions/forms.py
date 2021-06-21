from django.core.exceptions import ValidationError
from django.db.models.query import RawQuerySet
from django.forms import ModelForm, fields, widgets
from django import forms
from django.core.validators import MaxLengthValidator

from django.db.models import Avg, Max, Min, Sum
from .models import Bid, Listing, Category

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('bidder', 'article', 'amount')

    def clean(self):
        cleaned_data = super().clean()
        bidder = cleaned_data.get('bidder').first()
        article = cleaned_data.get('article').first()
        amount = cleaned_data.get('amount')

        if bidder == article.owner:
            raise ValidationError("the owner of the article cannot make a bid")
        
        if amount <= article.bids.all().aggregate(Max('amount')):
            raise ValidationError("Bid should be bigger than all previous bids")



class NewListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ["title", 'description', 'price' ,'photo']
        

    title = forms.CharField(label="Title", 
                            validators=[MaxLengthValidator(150)], required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Listing title', 'class': 'field form__field--long' , 'id': 'firstfield', 'autofocus':'autofocus'}))

    description = forms.CharField(label="Product Description's",
                                  widget=forms.Textarea(attrs={'placeholder': 'Write information about this article','class': 'field form__field--block'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True) ##widget=forms.Select(attrs={'class: form__field--select'}))

    price = forms.IntegerField(label="Initial Price", min_value=0, required=True,
                                widget= forms.NumberInput(attrs={'placeholder': 'Your bid','class': 'field form__field--number'}))
                            
    photo = forms.URLField(label="Product's photo URL",
                            widget= forms.URLInput(attrs={'placeholder': 'Photo URL', 'class': 'field form__field--long'}))

    