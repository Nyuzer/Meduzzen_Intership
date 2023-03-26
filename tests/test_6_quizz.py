from httpx import AsyncClient

# test3@test.com -> owner
# test1@test.com -> also member
# company_id == 2


async def test_get_quizzes_not_auth(ac: AsyncClient):
    response = await ac.get('/quizz/1')
    assert response.status_code == 403


async def test_get_quizzes_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quizz/1', headers=headers)
    assert response.status_code == 400


async def test_get_quizzes_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/100', headers=headers)
    assert response.status_code == 404


async def test_get_quizz_by_id_no_quizz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/1', headers=headers)
    assert response.status_code == 404


async def test_get_quizzes_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/2', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('quizzes')) == 0


# ------------------------------>


async def test_create_quizz_not_auth(ac: AsyncClient):
    response = await ac.post('/quizz/2/create')
    assert response.status_code == 403


async def test_create_quizz_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == 'Quizz can create only owner or admin'


async def test_create_quizz_not_success_number_of_frequency(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 0,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Number of frequency must be bigger than 0'


async def test_create_quizz_not_success_less_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 2,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Questions must bo more than 2'


async def test_create_quizz_not_success_less_answers(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 2,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'There must be more than 2 answers'


async def test_create_quizz_not_success_correct_answer_not_in_answers(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 2,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "5"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Correct answer not in answers'


async def test_create_qiuzz_not_admin_now_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "String12345",
        "description": "string description",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 400


async def test_create_quizz_success_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "name": "String123",
        "description": "string description",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_create_quizz_success_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "name": "String1234",
        "description": "string description",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_create_quizz_not_success_same_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "name": "String1234",
        "description": "string description",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/2/create', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == 'Quizz with this name already exist'


async def test_fetch_all_quizzes(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/2', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('quizzes')) == 2


async def test_create_quizz_not_success_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "string",
        "description": "string",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }
    response = await ac.post('/quizz/100/create', json=payload, headers=headers)
    assert response.status_code == 404


# ------------------------------>


async def test_get_quizz_by_id_no_quizz_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/3', headers=headers)
    assert response.status_code == 404


async def test_get_quizz_by_id_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/1', headers=headers)
    assert response.status_code == 400


async def test_get_quizz_by_id_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizz/100/quizz/1', headers=headers)
    assert response.status_code == 404


async def test_get_quizz_by_id_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('id') == 1


async def test_get_quizz_by_id_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('id') == 2


# ------------------------------>


async def test_update_quizz_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "number_of_frequency": 3
    }
    response = await ac.put('/quizz/100/update/2', json=payload, headers=headers)
    assert response.status_code == 404


async def test_update_quizz_no_quizz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "number_of_frequency": 4
    }
    response = await ac.put('/quizz/2/update/100', json=payload, headers=headers)
    assert response.status_code == 404


async def test_update_quizz_number_of_frequency_zero(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "number_of_frequency": 0
    }
    response = await ac.put('/quizz/2/update/2', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Frequency must be a positive number'


async def test_update_quizz_not_success_not_name(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "name": 'String123'
    }
    response = await ac.put('/quizz/2/update/2', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == 'Quizz with this name already exist'


async def test_update_quizz_not_success_not_owner_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "number_of_frequency": 5
    }
    response = await ac.put('/quizz/2/update/2', json=payload, headers=headers)
    assert response.status_code == 400


async def test_update_quizz_success_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "number_of_frequency": 5
    }
    response = await ac.put('/quizz/2/update/2', json=payload, headers=headers)
    assert response.status_code == 200


# ------------------------------>

# quizz = 2
payload = {
        "name": "String1234",
        "description": "string description",
        "number_of_frequency": 1,
        "quiz_questions": [
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            },
            {
                "question": "2+2=?",
                "answers": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct_answer": "4"
            }
        ]
    }


async def test_update_question_not_auth(ac: AsyncClient):
    response = await ac.put('/quizz/2/update/2/questions/4')
    assert response.status_code == 403


async def test_update_question_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'question': '2+4=?'
    }
    response = await ac.put('/quizz/100/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 404


async def test_update_question_no_quizz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'question': '2+4=?'
    }
    response = await ac.put('/quizz/2/update/100/questions/4', json=payload, headers=headers)
    assert response.status_code == 404


async def test_update_question_no_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'question': '2+4=?'
    }
    response = await ac.put('/quizz/2/update/2/questions/100', json=payload, headers=headers)
    assert response.status_code == 404


async def test_update_question_not_member_of_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        'question': '2+4=?'
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 400


async def test_update_question_not_admin_or_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        'question': '2+4=?'
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 400


async def test_update_question_answers_bad_length(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'answers': [
            "1",
            "2"
        ]
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail') == 'Answers should be more than two'


async def test_update_question_correct_answer_not_answers(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'answers': [
            "1",
            "2",
            "5"
        ]
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail') == 'Correct answer should be in answers'


async def test_update_question_correct_answer_not_answers_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'correct_answer': '102'
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json().get('detail') == 'Correct answer should be in answers'


async def test_update_question_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'question': '2+3=?'
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_update_question_success_answers_correct_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        'answers': [
            '3',
            '5',
            '6'
        ],
        'correct_answer': '5'
    }
    response = await ac.put('/quizz/2/update/2/questions/4', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_get_updated_quizz_with_questions(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quizz/2/quizz/2', headers=headers)
    assert response.status_code == 200


# ------------------------------>


async def test_delete_quizz_no_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/quizz/100/delete/2', headers=headers)
    assert response.status_code == 404


async def test_delete_quizz_no_quizz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/quizz/2/delete/100', headers=headers)
    assert response.status_code == 404


async def test_delete_quizz_not_onwer_not_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/quizz/2/delete/2', headers=headers)
    assert response.status_code == 400


async def test_delete_quizz_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/quizz/2/delete/2', headers=headers)
    assert response.status_code == 200


async def test_fetch_all_quizzes_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/quizz/2', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('quizzes')) == 1
