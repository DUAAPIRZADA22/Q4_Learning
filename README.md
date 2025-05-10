****API Parameters in FastAPI:****
API parameters are extra pieces of information that you send with a request to get specific results from the server.

**Why use parameters?**
1.To send details like:
2.Which item to get
3.How many items to skip
4.What data to add or update

**🧩 Types of Parameters in FastAPI**
FastAPI allows you to use many types of parameters. In this step, we will focus on:

Path Parameters: Part of the URL
Example: /items/{item_id}

Query Parameters: Added to the URL with ?
Example: /items?skip=0&limit=10

**Key Points to Remember:**
Use Path() for validating path parameters

Use Query() for validating query parameters

Both Path() and Query() support various validation options:

1.ge, gt, le, lt for numerical constraints
2.min_length, max_length for string length
3.regex or pattern for pattern matching
4.enum for restricting to a set of values
5.FastAPI will automatically validate all parameters according to your specifications
-- When validation fails, FastAPI returns a 422 Unprocessable Entity status code with detailed error information
