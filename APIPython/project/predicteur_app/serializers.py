from rest_framework import serializers
from predicteur_app.models import Incident


class IncidentSerializer(serializers.Serializer):
    """ to serialize or deserialize data
    -> Serialize                               : model instance / querysets => native Python datatypes => JSON
        ** NETWORK **
    -> Deserialize                             : JSON to model instance
    """

    active    = serializers.FloatField()
    incident_state    = serializers.FloatField()
    resolved_at   = serializers.FloatField()
    opened_at    = serializers.FloatField()
    number     = serializers.FloatField()
    sys_mod_count      = serializers.FloatField()
    u_priority_confirmation     = serializers.FloatField()

    duree    = serializers.FloatField(allow_null=True)

    def create(self, validated_data)           :
        """ Create and return a new 'House' instance, given the validated data """
        return Incident.objects.create(**validated_data)

    def update(self, instance, validated_data) :
        """ Update and return an existing 'Houste' instance, given the validated data """
        instance.active    = validated_data.get('active' , instance.active)
        instance.incident_state      = validated_data.get('incident_state' , instance.incident_state)
        instance.resolved_at   = validated_data.get('resolved_at' , instance.resolved_at)
        instance.opened_at    = validated_data.get('opened_at' , instance.opened_at)
        instance.number     = validated_data.get('number' , instance.number)
        instance.sys_mod_count      = validated_data.get('sys_mod_count' , instance.sys_mod_count)
        instance.u_priority_confirmation     = validated_data.get('u_priority_confirmation' , instance.u_priority_confirmation)
       
        #instance.MEDV   = validated_data.get('MEDV' , instance.MEDV)
        instance.save()
        return instance
