# from requests import Response
from flask import Flask,send_from_directory,request,jsonify,Response
import ee 
import json
from datetime import datetime,timedelta
# import logging
# logging.basicConfig(level=logging.DEBUG)
ee.Authenticate()
ee.Initialize(project="websen-468901")
app=Flask(__name__,static_folder='dist', static_url_path='')
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
@app.route("/data",methods=["POST"])    
def daata():
    # print("Request Received")
    global data
    data=request.get_json()
    return "Data received"

@app.route("/realtimemessage",methods=["get"])
def stream():
    def generate():
        if not data:
           yield "data :Invalid Data\n\n"
           return
        yield "data: Data received successfully\n\n"
        yield "data: Fetching data to Earth engine\n\n"
        try:
            polyjson=json.loads(data[0])
            polygon=ee.Geometry(polyjson["geometry"])
            info=polygon.getInfo()
            if polygon:
                yield "data: Polygon created successfully\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            return 
        try:
            sent1=(ee.ImageCollection("COPERNICUS/S1_GRD")
              .filterBounds(polygon)
              .filterMetadata('instrumentMode','equals','IW')
              .filterMetadata('transmitterReceiverPolarisation','equals',['VV','VH']))      
            sinfo=sent1.getInfo()
            if sent1:
               yield "data: Retrived image: filtered based on polygon\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            return 
        try:
           beend=datetime.strptime(data[1],"%Y-%m-%d")
           bestar=beend-timedelta(days=int(data[3]))
           beends=beend.strftime("%Y-%m-%d")
           bestars=bestar.strftime("%Y-%m-%d")
           befsen=sent1.filterDate(bestars,beends)
           if befsen:
              yield "data: Retrived image: filtered based on preincident date\n\n"
        # sinfo=befsen.getInfo()
        # return jsonify({"success":sinfo})
        except Exception as e:
           yield f"data: Error: {str(e)}\n\n"
           return 
        try:
            afstar=datetime.strptime(data[2],"%Y-%m-%d")
            afend=afstar+timedelta(days=int(data[4]))
            afstars=afstar.strftime("%Y-%m-%d")
            afends=afend.strftime("%Y-%m-%d")
            afsen=sent1.filterDate(afstars,afends)
            if afsen:
               yield "data: Retrived image: filtered based on postincident date\n\n"
            # sinfo=afsen.getInfo()
            # return jsonify({"success":sinfo})    
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            return 
        # 
        # yield f"data:Postincident Images Number: {afsen.size().getInfo()}\n\n"
        try:
           l=[]
           try:
               yield f"data:Preincident Images Number: {befsen.size().getInfo()}\n\n"
           except:
               l.append("No Preincident Image")
           try:
               yield f"data:Postincident Images Number: {afsen.size().getInfo()}\n\n"
           except:
               l.append("No Postincident Image")
           if len(l)==0:
               yield "data:Preprocessing images\n\n"
           if len(l)==1:
               yield f"data:{l[0]}\n\n"
           if len(l)==2:
               yield f"data:{l[0]}&&{l[1]}\n\n"
        except Exception as e:
            return
            
       

    return Response(generate(), content_type="text/event-stream")      
# app=Flask(__name__)
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)




