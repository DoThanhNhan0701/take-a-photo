import json
import os

def generate_postman_collection():
    collection = {
        "info": {
            "name": "Take a Photo API",
            "description": "API collection for Take a Photo application",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Auth",
                "item": [
                    {
                        "name": "Login",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "var jsonData = pm.response.json();",
                                        "pm.environment.set(\"access_token\", jsonData.access_token);",
                                        "pm.environment.set(\"refresh_token\", jsonData.refresh_token);"
                                    ],
                                    "type": "text/javascript"
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "username": "testuser",
                                    "password": "testpass123"
                                }, indent=4)
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/auth/login",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "auth", "login"]
                            }
                        }
                    },
                    {
                        "name": "Refresh Token",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "var jsonData = pm.response.json();",
                                        "pm.environment.set(\"access_token\", jsonData.access_token);",
                                        "pm.environment.set(\"refresh_token\", jsonData.refresh_token);"
                                    ],
                                    "type": "text/javascript"
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "refresh_token": "{{refresh_token}}"
                                }, indent=4)
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/auth/refresh",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "auth", "refresh"]
                            }
                        }
                    },
                    {
                        "name": "Get Me",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/v1/auth/me",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "auth", "me"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Users",
                "item": [
                    {
                        "name": "List Users",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/v1/users/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "users", ""]
                            }
                        }
                    },
                    {
                        "name": "Create User",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "username": "newuser",
                                    "email": "newuser@example.com",
                                    "password": "password123",
                                    "full_name": "New User",
                                    "role": "staff"
                                }, indent=4)
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/users/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "users", ""]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Locations",
                "item": [
                    {
                        "name": "List Locations",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/v1/locations/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "locations", ""]
                            }
                        }
                    },
                    {
                        "name": "Create Location",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "name": "New Store",
                                    "code": "NS_001",
                                    "address": "123 Street, City",
                                    "gps_latitude": 16.0544,
                                    "gps_longitude": 108.2022
                                }, indent=4)
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/locations/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "locations", ""]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Categories",
                "item": [
                    {
                        "name": "List Categories",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/v1/categories/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "categories", ""]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Invoices",
                "item": [
                    {
                        "name": "List Invoices",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/v1/invoices/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "invoices", ""]
                            }
                        }
                    },
                    {
                        "name": "Create Invoice",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "var jsonData = pm.response.json();",
                                        "pm.environment.set(\"invoice_id\", jsonData.id);"
                                    ],
                                    "type": "text/javascript"
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "location_id": "REPLACE_WITH_LOCATION_UUID",
                                    "category_id": 1,
                                    "note": "Test invoice from Postman",
                                    "status": "draft"
                                }, indent=4)
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/invoices/",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "invoices", ""]
                            }
                        }
                    },
                    {
                        "name": "Upload Image",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{access_token}}"}
                            ],
                            "body": {
                                "mode": "formdata",
                                "formdata": [
                                    {
                                        "key": "file",
                                        "type": "file",
                                        "src": []
                                    },
                                    {
                                        "key": "gps_latitude",
                                        "value": "16.0544",
                                        "type": "text"
                                    },
                                    {
                                        "key": "gps_longitude",
                                        "value": "108.2022",
                                        "type": "text"
                                    }
                                ]
                            },
                            "url": {
                                "raw": "{{base_url}}/api/v1/invoices/{{invoice_id}}/images",
                                "host": ["{{base_url}}"],
                                "path": ["api", "v1", "invoices", "{{invoice_id}}", "images"]
                            }
                        }
                    }
                ]
            }
        ],
        "variable": [
            {
                "key": "base_url",
                "value": "http://127.0.0.1:8000",
                "type": "string"
            }
        ]
    }
    
    with open("postman_collection.json", "w") as f:
        json.dump(collection, f, indent=4)
    
    print("Successfully generated 'postman_collection.json'")

if __name__ == "__main__":
    generate_postman_collection()
