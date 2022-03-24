from django.db import models
import numpy as np
import pymc as pm

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=5000)
    choices = models.TextField(max_length=20000)
    answer = models.CharField(max_length=2)
    difficulty = models.FloatField()

    objects = models.Manager()

    def __str__(self):
        return '%s. %s \t Difficulty: (%s)\n %s' % (self.id,self.question,self.difficulty,self.choices)

    def evalIRF(self,theta):
        return 1/(1+np.exp(-1*(theta*10-self.difficulty)))

    def evaldIRF(self,theta):
        e = 2.718
        return 10*(np.log(e)*np.exp(-1*(theta*10-self.difficulty)))/np.power((1+np.exp(-1*(theta*10-self.difficulty))),2)
    
    def evalIIF(self, theta):
        dp = self.evaldIRF(theta)
        p = self.evalIRF(theta)
        return np.power(dp,2)/(p*(1-p))

class Learner(models.Model):
    name = models.CharField(max_length=150)
    responses = models.TextField(null=True,blank=True)
    ability = models.FloatField()
    answered = models.TextField(null=True,blank=True)

    objects = models.Manager()
    
    def __str__(self):
        return '%s \t Ability: %s' %(self.name,self.ability)

    def updateAbility(self,question,data,theta):
        @pm.deterministic
        def p(theta=theta):
            return 1.0/(1+np.exp(-1*(theta*10-question.difficulty)))
        x = pm.Bernoulli('x',p,value=data[-1],observed=True)
        model = pm.Model([theta, p, x])
        m = pm.MAP(model)
        m.fit()
        self.ability = float('%.4f'%m.get_node('theta').value)

    def update(self,question,data,theta):
        @pm.deterministic
        def p(theta=theta):
            return 1.0/(1+np.exp(-1*(theta*10-question.difficulty)))
        x = pm.Bernoulli('x',p,value=data,observed=True)
        model = pm.Model([theta, p, x])
        m = pm.MAP(model)
        m.fit()
        self.ability = float('%.4f'%m.get_node('theta').value)

    def getList(self,l):
        if l:
            return [int(elem) for elem in list(l) if elem != ',']
        else:
            return None

    def setList(self,l):
        convertedString = ''
        if l:
            for elem in l:
                convertedString += (str(elem)+',')
        return convertedString