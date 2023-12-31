from rest_framework.response                    import Response
from rest_framework.decorators                  import action
from rest_framework                             import status, viewsets
from django.contrib.auth.models                 import User
from django.db.models                           import Q
from .serializers                               import *
from .models                                    import *
from django.utils import timezone
from datetime import datetime
from functools import reduce
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def create_user(self, *args, **kwargs):
        req = self.request.data

        first_name = req.get('first_name')
        last_name = req.get('last_name')
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')

        if not (username and first_name and last_name and email and password):
            return Response({'message': 'Preencha todos os campos.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=req)
        if serializer.is_valid():
            try:
                user = User(
                    username=username,
                    first_name=first_name,
                    email=email,
                    last_name=last_name,
                    is_active=True,
                    is_superuser=False
                )
                user.set_password(password)
                user.save()
                return Response({'message': 'Usuário cadastrado!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    def me(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        my_datas = self.queryset.get(pk=user_id)

        serializer = self.serializer_class(my_datas)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer

    @action(detail=False, methods=['post'])
    def create_company(self, *args, **kwargs):
        req = self.request.data
        cnpj = req.get("cnpj")
        razao_social = req.get("razao_social")
        nome_fantasia = req.get("nome_fantasia")
        area_de_atuacao = req.get("area_de_atuacao")
        tempo_atuacao_mercado = req.get("tempo_atuacao_mercado")
        capital_social = req.get("capital_social")
        n_func_clt = req.get("n_func_clt")
        n_func_terc = req.get("n_func_terc")
        n_estagiario = req.get("n_estagiario")
        n_socios = req.get("n_socios")
        nome_socios = req.get("nome_socios")
        website = req.get("website")
        instagram = req.get("instagram")
        facebook = req.get("facebook")
        twitter = req.get("twitter")
        linkedin = req.get("linkedin")
        email = req.get("email")

        if not (cnpj or razao_social or nome_fantasia or nome_fantasia or area_de_atuacao or tempo_atuacao_mercado or capital_social or n_func_clt or n_func_terc or n_socios or razao_social):
            return Response({'detail': 'Campos marcados são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        print(tempo_atuacao_mercado)
        empresario = User.objects.get(pk=1)
        serializer = CompanySerializer(data=req)

        if serializer.is_valid():
            try:
                company = CompanyModel(
                    cnpj = cnpj,
                    razao_social = razao_social,
                    nome_fantasia = nome_fantasia,
                    area_de_atuacao = area_de_atuacao,
                    tempo_atuacao_mercado = int(tempo_atuacao_mercado),
                    capital_social = float(capital_social),
                    n_func_clt = int(n_func_clt),
                    n_func_terc = int(n_func_terc),
                    n_estagiario = int(n_estagiario),
                    n_socios = int(n_socios),
                    nome_socios = nome_socios,
                    website = website,
                    instagram = instagram,
                    facebook = facebook,
                    twitter = twitter,
                    linkedin = linkedin,
                    email = email
                )
                company.save()
                return Response({'message': 'Empresa cadastrada!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': serializer.errors, 'message': 'Houveram erros de validação'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=False)
    def get_company(self, *args, **kwargs):
        company_id = self.request.query_params.get('company_id', None)
        try:
            company = self.queryset.get(pk=company_id)
            serializer = self.serializer_class(company)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Dados não encontrados.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False)
    def get_sum_invoicing_per_year(self, *args, **kwargs):

        try:
            invoicings = InvoicingModel.objects.all()
            dados_por_ano = {}

            for dado in invoicings:
                data = str(dado.date)[:4]
                if data not in dados_por_ano:
                    dados_por_ano[data] = []
                dados_por_ano[data].append({
                    'id': dado.id,
                    'date': dado.date,
                    'value': dado.value
                })
            soma_ano = []
            for i in dados_por_ano:
                soma = reduce(lambda acumulador, valores: valores['value'] + acumulador, dados_por_ano[i], 0)
                soma_ano.append({
                    "ano": i,
                    "valor": soma
                })
            return Response(data=soma_ano, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Dados não encontrados.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False)
    def get_invoicing_per_year(self, *args, **kwargs):
        company_id = self.request.query_params.get('company_id', None)
        ano = self.request.query_params.get('ano', None)
        try:
            invoicings = InvoicingModel.objects.filter(company__id=company_id).order_by('date')
            dados_por_ano = {}

            for dado in invoicings:
                data = str(dado.date)[:4]
                if data not in dados_por_ano:
                    dados_por_ano[data] = []
                dados_por_ano[data].append({
                    'id': dado.id,
                    'date': dado.date,
                    'value': dado.value
                })
            
            return Response(data=dados_por_ano[ano], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Dados não encontrados.'}, status=status.HTTP_404_NOT_FOUND)
        
        

    @action(methods=['GET'], detail=False)
    def get_quarterly_billing(self, *args, **kwargs):
        company_id = self.request.query_params.get('company_id', None)
        ano = self.request.query_params.get('ano', None)
        try:
            invoicings = InvoicingModel.objects.all().order_by('-date')
            dados_por_ano = {}

            for dado in invoicings:
                data = str(dado.date)[:4]
                if data not in dados_por_ano:
                    dados_por_ano[data] = []
                dados_por_ano[data].append({
                    'id': dado.id,
                    'date': dado.date,
                    'value': dado.value
                })
            ano_de_retorno = dados_por_ano[ano]
            por_mes = {}
            for dado in ano_de_retorno:
                data = str(dado['date'])[:7]
                if data not in por_mes:
                    por_mes[data] = []
                por_mes[data].append({
                    'id': dado['id'],
                    'date': dado['date'],
                    'value': dado['value']
                })
            soma_mes = []
            for i in por_mes:
                soma = reduce(lambda acumulador, valores: valores['value'] + acumulador, por_mes[i], 0)
                soma_mes.append({
                    "mes": i[5:7],
                    "valor": soma
                } )
            return Response(data=soma_mes, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Dados não encontrados.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False)
    def get_total_employees(self, *args, **kwargs):
        companyes = self.queryset
        num_func = 0
        for i in companyes:
            num_func+= i.n_func_clt + i.n_estagiario + i.n_func_terc
        return Response(data={'total': num_func}, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False)
    def get_total_invoicing(self, *args, **kwargs):
        company_id = self.request.query_params.get('company_id', None)

        try:
            invoicings = InvoicingModel.objects.all()
            dados_por_ano = {}

            for dado in invoicings:
                data = str(dado.date)[:4]
                if data not in dados_por_ano:
                    dados_por_ano[data] = []
                dados_por_ano[data].append({
                    'id': dado.id,
                    'date': dado.date,
                    'value': dado.value
                })
            soma_ano = {}
            for i in dados_por_ano:
                soma = reduce(lambda acumulador, valores: valores['value'] + acumulador, dados_por_ano[i], 0)
                soma_ano['ano_'+i] = {
                    "valor_somado": soma
                }
            return Response(data=soma_ano, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Dados não encontrados.'}, status=status.HTTP_404_NOT_FOUND)

        