#### Tests for CRUD service for bears in alaska

Service downloaded from  [docker](https://hub.docker.com/r/azshoo/alaska)

Started with
```markdown 
docker run -d -p 8091:8091 -it azshoo/alaska:1.0
```

Used modules listed in requirements.txt

#####Create bear
parametrize by *{bear_name}*: 'Tedd', 'tedd', 'ИмяМедведя', 'медведь123'

parametrize by *{bear_type}*: 'BLACK', 'BROWN', 'POLAR', 'GUMMY'

parametrize by *{bear_age}*: 0, 1, 49.5, 100, '0.1', '1.7', '99.999'

| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": *{type}*, "bear_name": *{name}*, "bear_age": *{age}*} | status code 200              |
| 2    | Get exist bear by id              | GET 0.0.0.0:8091/bear/step 1 id                                                 | Check that exist bear equal to expected |

#####Create bear unsuccessfully by age
parametrize by *{bear_age}*: -1, 101, 99999.99999

| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": 'Tedd', "bear_age": *{age}*} | status code 200                 |
| 2    | Get exist bear by id              | GET 0.0.0.0:8091/bear/step 1 id                                                 | Check that bear age equal to 0          |


#####Create bear unsuccessfully internal error
| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": 'NotExistedType', "bear_name": 'Tedd', "bear_age": 10 | Internal Server Error           |

| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": null, "bear_name": 'Tedd', "bear_age": 10 | Internal Server Error           |

| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": 'Tedd', "bear_age": null | Internal Server Error           |

| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": null, "bear_age": 10 | Internal Server Error           |


#####Delete all bears
| step | description                       | request                         | expected result                  |
|------|-----------------------------------|---------------------------------|----------------------------------|
| 1    | Create 10 new bears                     | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": 'Tedd', "bear_age": 10           | status code 200     |
| 2    | Get all bears before create new        | GET 0.0.0.0:8091/bear | remember bears count                            |
| 3    | Delete bears        | DELETE 0.0.0.0:8091/bear | OK                            |
| 4    | Get all bears after delete"        | GET 0.0.0.0:8091/bear | step2 bears count - 10 == step4 bears count                            |


#####Delete exist bear
| step | description                       | request                                                                                                                           | expected result                  |
|------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| 1    | Get all bears before create new   | GET 0.0.0.0:8091/bear                                                                                                             | remember bears count             |
| 2    | Create new bear            | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": 'Tedd', "bear_age": 10  | status code 200                  |
| 3    | Get exist bear by id              |    GET 0.0.0.0:8091/bear/step2 id                                                                                                | equal to step2   |
| 4    | Delete bear    | DELETE 0.0.0.0:8091/bear/ step2 id                                                                                                             | OK             |
| 5    | Get exist bear by id |        GET 0.0.0.0:8091/bear/step2 id                                                                                                                             | EMPTY |
| 6    | Get all bears after delete"        | GET 0.0.0.0:8091/bear | step1 bears count == step6 bears count                            |


#####Update bear
parametrize by *{bear_name}*: 'Tedd', 'TEDD', '123', '', ' ', '\r\n'

parametrize by *{bear_type}*: 'BROWN', 'POLAR', 'GUMMY', 'TEST'

parametrize by *{bear_age}*: '11', 11, 111, -1


| step | description                       | request                                                                         | expected result                         |
|------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear {"bear_type": 'BLACK', "bear_name": 'Tedd', "bear_age": 1} | status code 200                 |
| 2    | Update bear by id             | POST 0.0.0.0:8091/bear/step 1 id {"bear_type": *{type}*, "bear_name": *{name}*, "bear_age": *{age}*}  | status code 200          |
| 3    | Get exist bear by id              |    GET 0.0.0.0:8091/bear/step2 id                               | equal to step2   |

#####Get all bears
| step | description                       | request                                                                                                                           | expected result                  |
|------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| 1    | Get all bears before create new   | GET 0.0.0.0:8091/bear                                                                                                             | remember bears count             |
| 2    | Create new random bear            | POST 0.0.0.0:8091/bear {"bear_type": POLAR, BROWN, BLACK or GUMMY, "bear_name": random english chars, "bear_age": from 0 to 100} | status code 200                  |
| 3    | Check new bear unique             |                                                                                                                                   | no bear with same params in DB   |
| 4    | Get all bears after create new    | GET 0.0.0.0:8091/bear                                                                                                             | remember bears count             |
| 5    | Check that new bear present in DB |                                                                                                                                   | new bear exit in response step 4 |
| 6    | Check bears count                 |                                                                                                                                   | step1 count < step4 count      |

#####Get exist bear
| step | description                       | request                                                                                                                           | expected result                         |
|------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| 1    | Create new bear                   | POST 0.0.0.0:8091/bear  {"bear_type": POLAR, BROWN, BLACK or GUMMY, "bear_name": random english chars, "bear_age": from 0 to 100} | status code 200                         |
| 2    | Get exist bear by id              | GET 0.0.0.0:8091/bear/step 1 id                                                                                                   | Check that exist bear equal to expected |

#####Get not exist bear
| step | description                       | request                         | expected result                  |
|------|-----------------------------------|---------------------------------|----------------------------------|
| 1    | Get all bears                     | GET 0.0.0.0:8091/bear           | generate not existed bear id     |
| 2    | Get not existed bear by id        | GET 0.0.0.0:8091/bear/step 1 id | EMPTY                            |