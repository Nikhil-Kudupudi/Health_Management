from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json
# Create your views here.
@csrf_exempt
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
                 return render(request, 'management_mongo/results.html', {
                    'error': "No query provided",
                })
            
            client=MongoClient("mongodb://localhost:27017/")
            db=client['healthmanagement']
            
            output=db[query].find({})
            columns=output[0].keys
            values=[list(row.values()) for row in output]
            # return JsonResponse(results, safe=False)
            # Pass results and columns to the template
            
            return render(request, 'management_mongo/results.html', {
                    'query':query,
                    'results': output,
                    "columns":columns,
                    "values":values
                })
        
        except Exception as e:
        # return JsonResponse({"error": str(e)}, status=500)
            print(e)
            return render(request, 'management_mongo/results.html', {
                'query':query,
                    'error': str(e),
                })
    return render(request, 'management_mongo/results.html',{
        'query': query,
        'results': results,
        'columns': columns,
        'error': error
    })
