from django import forms
from aol.models import Document, Lake, LakeCounty

class LakeForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        """
        We need to override the save method because of the LakeCounty m2m
        table
        """
        kwargs['commit'] = False
        super(LakeForm, self).save(*args, **kwargs)
        self.instance.save()
        # save the m2m
        # delete all existing counties
        LakeCounty.objects.filter(lake=self.instance).delete()
        # add all the counties from the form
        for county in self.cleaned_data['county_set']:
            LakeCounty(lake=self.instance, county=county).save()

    class Meta:
        model = Lake
        fields = (
            'title',
            'body',
            'gnis_id',
            'gnis_name',
            'reachcode',
            'fishing_zone',
            'huc6',
            'county_set',
        )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'name',
            'file',
            'rank',
        )

