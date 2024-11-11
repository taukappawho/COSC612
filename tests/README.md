# Backend tests
## 6 tests for Use Case 1
| Test ID | Input                              | Expected Result                                    | Use Case |
|:---------:|------------------------------------|----------------------------------------------------|:----------:|
| 1.1     | (User with none, Admin logged in)  | User’s authorization raised to user                | 1        |
| 1.2     | (User with user, Admin logged in)  | User’s authorization raised to admin               | 1        |
| 1.3     | (User with admin, Admin logged in) | Authorization remains admin; no change             | 1        |
| 1.4     | (Invalid User, Admin logged in)    | Error: User does not exist                         | 1        |
| 1.5     | (Valid User, Admin not logged in)  | Error: Must have Admin privileges and be logged in | 1        |
| 1.6     | (User with invalid authorization level) | Error: Invalid authorization level provided | 1        |


## 7 tests for Use Case 2
### Uses postman to connect to the server
Tests written and documented by Jamie Cooper
###### (modularity could be greatly improved)
