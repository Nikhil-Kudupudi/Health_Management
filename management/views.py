from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
@csrf_exempt
# @require_http_methods(["POST","GET"])  
def run_direct_query(request):
    query = None  # Default query value
    results = None
    columns = None
    error = None
    if request.method == "POST":
        try:
        # Parse the body as JSON
            # body = json.loads(request.body)
            #  query = body.get("query")  # Extract the SQL query from the JSON payload
            query = request.POST.get('query')

            if not query:
            # return JsonResponse({"error": "No query provided"}, status=400)
                 return render(request, 'management/results.html', {
                    'error': "No query provided",
                })

        # Execute query
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]  # Get column names
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Format rows as dictionaries

        # return JsonResponse(results, safe=False)
            # Pass results and columns to the template
                return render(request, 'management/results.html', {
                    'query':query,
                    'results': results,
                    'columns': columns,
                })
        
        except Exception as e:
        # return JsonResponse({"error": str(e)}, status=500)
            print(e)
            return render(request, 'management/results.html', {
                'query':query,
                    'error': str(e),
                })
    return render(request, 'management/results.html',{
        'query': query,
        'results': results,
        'columns': columns,
        'error': error
    })


def get_visuals(request):
    Hospital_frequency_query=""" SELECT HospitalName , ( SELECT COUNT(*) FROM appointment a WHERE a.Hospital_ID = 
h.HospitalID  ) as Frequency
        FROM hospital h  
        WHERE ( 
            SELECT COUNT(*) FROM appointment a WHERE a.Hospital_ID = 
h.HospitalID 
        ) > ( 
            SELECT AVG(TotalAppointments) FROM ( 
                SELECT COUNT(*) AS TotalAppointments FROM appointment GROUP 
BY Hospital_ID 
            ) AS AvgAppointments 
        );"""
    cursor=connection.cursor()
    #hospital_frequency_query
    cursor.execute(Hospital_frequency_query)
    columns = [col[0] for col in cursor.description]  # Get column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]  
    df=pd.DataFrame(results)
    # Generate the plot
    plt.figure(figsize=(8, 6))
    plt.bar(df['HospitalName'], df['Frequency'])
    plt.title('Query Results Visualization')
    plt.xlabel('Hospital Name')
    plt.ylabel('Number Of appointments')
    plt.grid(False)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    #appointments timeline
    appointment_timeline="""
select AppointmentDate, count(*)  as Frequency
from appointment
group by AppointmentDate;
"""
    cursor.execute(appointment_timeline)
    columns = [col[0] for col in cursor.description]  # Get column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]  
    df=pd.DataFrame(results)
    df['Month']=pd.to_datetime(df['AppointmentDate']).dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
    frequency = df['Month'].value_counts().reindex(month_order, fill_value=0)
    # Generate the plot
    plt.figure(figsize=(8, 6))
    plt.plot(frequency.index, frequency.values)
    plt.title('Query Results Visualization')
    plt.xlabel('AppointmentDate')
    plt.ylabel('Number Of appointments')
    plt.xticks(rotation=45)
    plt.grid(False)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image2_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return render(request,'management/dashboard.html',{'charts':[image_base64,image2_base64]})
    # return  JsonResponse(results, safe=False)