from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
# Create your views here.
from .forms import TopsisForm
import pandas as pd
import numpy as np
from django.core.files.storage import default_storage
from .models import TopsisAnalysis, TopsisResult
import json
def loginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/topsis')
        else:
            return render(request, 'topsis_app/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'topsis_app/login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

def topsis_algorithm(input_file, weights, impacts):
    data = pd.read_csv(input_file)
    impacts = impacts.replace(", ", "")
    weights  = weights.replace(", ","")
    weights = [int(element) for element in weights]
    impacts = list(impacts)
    
    # Validate input
    if len(weights) != len(data.columns) - 1 or len(impacts) != len(data.columns) - 1:
        raise ValueError("Invalid input length")
    
    # Apply TOPSIS
    for i in range(1, len(data.columns)):
        data.iloc[:, i] = data.iloc[:, i] * (-1 if impacts[i-1] == '-' else 1)
        
    norm_data = data.iloc[:, 1:].apply(lambda x: x / np.linalg.norm(x), axis=0)
    weighted_data = norm_data * weights

    ideal_best = weighted_data.max()
    ideal_worst = weighted_data.min()

    dist_best = np.linalg.norm(weighted_data - ideal_best, axis=1)
    dist_worst = np.linalg.norm(weighted_data - ideal_worst, axis=1)

    topsis_score = dist_worst / (dist_best + dist_worst)
    rank = np.argsort(topsis_score)[::-1] + 1

    data['Topsis Score'] = topsis_score
    data['Rank'] = rank

    table_style = '''
    <style>
        table {
            width: 60%;
            margin: 20px auto;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
        }
        th, td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            color: #000;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
    '''
    data["Model Name"] = data.iloc[:, 0]
    table_html = data[['Model Name', 'Topsis Score', 'Rank']].to_html(classes='dataframe', index=False)
    full_html = table_style + table_html
    return full_html, data
    
def topsis_view(request):
    if request.user.is_anonymous:
        return redirect('/login')
    result = None
    form = TopsisForm()
    if request.method == 'POST':
        form = TopsisForm(request.POST, request.FILES)
        if form.is_valid():
            input_file = request.FILES['input_file']
            weights = form.cleaned_data['weights']
            impacts = form.cleaned_data['impacts']
            analysis = TopsisAnalysis.objects.create(
                user=request.user,
                input_file=input_file.name,
                weights=weights,
                impacts=impacts
            )
            try:
                result, results_data = topsis_algorithm(input_file, weights, impacts)                
                topsis_result = TopsisResult.objects.create(
                    analysis=analysis,
                    topsis_score=results_data['Topsis Score'].to_json(),
                    rank=results_data['Rank'].to_json()
                )
            except Exception as e:
                return render(request, 'topsis_app/index.html', {'form': form, 'error': str(e)})
    return render(request, 'topsis_app/index.html', {'form': form, 'result': result})   

def user_history_view(request):
    user_analysis = TopsisAnalysis.objects.filter(user=request.user).order_by('-date')
    return render(request, 'topsis_app/history.html', {'analyses': user_analysis})

def view_analysis(request, id):
    analysis = get_object_or_404(TopsisAnalysis, id=id)
    result = TopsisResult.objects.get(analysis=analysis)
    topsis_score = json.loads(result.topsis_score)
    rank = json.loads(result.rank)
    
    return render(request, 'topsis_app/result.html', {
        'analysis': analysis,
        'topsis_score': topsis_score,
        'rank': rank,
    })