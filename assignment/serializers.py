from django.db.utils import IntegrityError
from rest_framework import serializers
from classroom.models import Class
from classroom.serializers import UserSerializer
from .models import Question, Assignment, GradedAssignment


class AssignmentSerializer(serializers.ModelSerializer):
    num_questions = serializers.IntegerField(default=0)

    class Meta:
        model = Assignment
        fields = ('id', 'title', 'created_on', 'num_questions')


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.IntegerField(
        write_only=True, max_value=4, min_value=1)

    class Meta:
        model = Question
        fields = ('id', 'text', 'c1', 'c2', 'c3', 'c4', 'answer')


class AssignmentDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    classroom = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=Class.objects.all().select_related('created_by'))

    def create(self, validated_data):
        try:
            questions = validated_data.pop('questions')
            a = Assignment.objects.create(**validated_data)
            Question.objects.bulk_create([Question(**data, assignment=a) for data in questions])
        except:
            a.delete()
            raise serializers.ValidationError({'detail': 'Something unexpected happened.'})
        return a

    def validate_classroom(self, value):
        if value.created_by == self.context['request'].user:
            return value
        raise serializers.ValidationError('You cannot post assignment to this classroom.')

    class Meta:
        model = Assignment
        fields = ('id', 'title', 'questions', 'created_on', 'classroom')


class GradedAssignmentSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=4), write_only=True)
    user = UserSerializer(read_only=True)

    def create(self, vd):
        reason = None
        try:
            ans = vd.pop('answers')
            a = Assignment.objects.prefetch_related("questions").get(pk=vd['a_pk'])
            total = 0
            marks = 0
            for q in a.questions.all():
                if q.answer == ans[total]:
                    marks += 1
                total += 1
            g_assignment = GradedAssignment.objects \
                .create(assignment=a, total_marks=total, marks=marks, user=vd['user'])
        except IndexError:
            reason = "Answer all the questions."
        except Assignment.DoesNotExist:
            reason = 'Assignment does not exist.'
        except IntegrityError:
            reason = 'You already submitted the assignment.'
        except:
            reason = 'Something unexpected happened.'
        finally:
            if reason is not None:
                raise serializers.ValidationError({'detail': reason})
        return g_assignment

    class Meta:
        model = GradedAssignment
        fields = '__all__'
        read_only_fields = ('marks', 'total_marks', 'user', 'assignment')
