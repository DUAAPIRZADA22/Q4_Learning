****API Parameters in FastAPI:****

API parameters are extra pieces of information that you send with a request to get specific results from the server.

**Why use parameters?**

1.To send details like:

2.Which item to get

3.How many items to skip

4.What data to add or update

**🧩 Types of Parameters in FastAPI**:

FastAPI allows you to use many types of parameters. In this step, we will focus on:

1.Path Parameters: Parts of the URL path that are variable (e.g., /items/{item_id})

2. Query Parameters: Parameters appended to the URL after a ? (e.g., /items?skip=0&limit=10)
   
3. Request Body: Data sent in the body of the request (usually in JSON format)
   
4.  Headers: Custom HTTP headers sent with the request
   
5. Cookies: Data sent in the Cookie header
   
6. Form Data: Fields submitted in a form
    
7.  File Uploads: Files uploaded in a form



**Key Points to Remember:**
1. Use Path() for validating path parameters
2. Use Path() for validating path parameters
3. Both Path() and Query() support various validation options
4. FastAPI will automatically validate all parameters according to your specifications
5. When validation fails, FastAPI returns a 422 Unprocessable Entity status code with detailed error information
   
