import os
import unittest

# app 을 가져오기 전에 메모리 데이터베이스를 고릅니다. instance/todo.db 를 건드리지 않습니다.
os.environ["TODO_DATABASE_URI"] = "sqlite:///:memory:"

import app as todo_app  # noqa: E402  (위의 환경 변수를 먼저 정해야 한다)


class TodoApiTest(unittest.TestCase):

    def setUp(self):                    # 테스트 하나마다 먼저 돈다
        todo_app.app.config["TESTING"] = True
        self.client = todo_app.app.test_client()
        self.ctx = todo_app.app.app_context()
        self.ctx.push()
        todo_app.db.drop_all()
        todo_app.db.create_all()

    def tearDown(self):                 # 끝날 때마다 돈다
        todo_app.db.session.remove()
        self.ctx.pop()

    # ---- 2차시 47쪽 일곱 가지 (L7-3 74쪽의 다섯 개)
    def test_만든_것이_목록에_그대로_나온다(self):
        self.client.post("/api/todos/", json={"text": "우유 사기", "done": True})
        self.client.post("/api/todos/", json={"text": "책 반납"})
        r = self.client.get("/api/todos/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 2)          # 둘 다 나와야 한다

    def test_만들면_201_과_만들어진_것이_온다(self):
        r = self.client.post("/api/todos/", json={"text": "우유 사기"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["text"], "우유 사기")

    def test_없는_번호는_404_다(self):
        r = self.client.get("/api/todos/999")
        self.assertEqual(r.status_code, 404)

    def test_patch_는_보낸_칸만_바꾼다(self):
        made = self.client.post("/api/todos/", json={"text": "책 반납"}).get_json()
        r = self.client.patch(f"/api/todos/{made['id']}", json={"done": True})
        self.assertEqual(r.get_json()["text"], "책 반납")    # 글자는 그대로
        self.assertTrue(r.get_json()["done"])                # 완료만 바뀜

    def test_지우면_204_고_다시_찾으면_404_다(self):
        made = self.client.post("/api/todos/", json={"text": "지울 것"}).get_json()
        self.assertEqual(self.client.delete(f"/api/todos/{made['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/todos/{made['id']}").status_code, 404)

    # ---- HW4 에서 더한 것 : note 칸, ?done= 필터링, 문서
    def test_note_를_넣어_만들면_그대로_돌아온다(self):
        r = self.client.post("/api/todos/", json={"text": "우유 사기", "note": "2리터짜리로"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["note"], "2리터짜리로")
        self.assertFalse(r.get_json()["done"])

    def test_note_를_안_보내면_빈_글자다(self):
        r = self.client.post("/api/todos/", json={"text": "책 반납"})
        self.assertEqual(r.get_json()["note"], "")

    def test_patch_로_done_만_바꾸면_text_와_note_는_그대로다(self):
        made = self.client.post("/api/todos/", json={"text": "우유 사기", "note": "2리터짜리로"}).get_json()
        r = self.client.patch(f"/api/todos/{made['id']}", json={"done": True})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["text"], "우유 사기")
        self.assertEqual(r.get_json()["note"], "2리터짜리로")
        self.assertTrue(r.get_json()["done"])

    def test_done_필터링은_골라서_주고_안_붙이면_전부_준다(self):
        self.client.post("/api/todos/", json={"text": "우유 사기", "done": True})
        self.client.post("/api/todos/", json={"text": "책 반납"})
        done = self.client.get("/api/todos/?done=true").get_json()
        undone = self.client.get("/api/todos/?done=false").get_json()
        every = self.client.get("/api/todos/").get_json()
        self.assertEqual([t["text"] for t in done], ["우유 사기"])
        self.assertEqual([t["text"] for t in undone], ["책 반납"])
        self.assertEqual(len(every), 2)                  # 69쪽에서 깨졌던 그 경우

    def test_없는_번호의_404_는_message_json_이다(self):
        r = self.client.get("/api/todos/999")
        self.assertEqual(r.get_json(), {"message": "999 번 할 일이 없습니다"})

    def test_text_없이_만들면_400_이다(self):
        r = self.client.post("/api/todos/", json={"note": "글자가 없다"})
        self.assertEqual(r.status_code, 400)

    def test_문서가_열린다(self):
        self.assertEqual(self.client.get("/api/docs").status_code, 200)
        self.assertEqual(self.client.get("/api/swagger.json").status_code, 200)

    def test_put_은_보내지_않은_칸을_기본값으로_되돌린다(self):
        made = self.client.post("/api/todos/", json={"text": "우유 사기", "done": True, "note": "메모"}).get_json()
        r = self.client.put(f"/api/todos/{made['id']}", json={"text": "우유 사기"})
        self.assertFalse(r.get_json()["done"])
        self.assertEqual(r.get_json()["note"], "")


if __name__ == "__main__":
    unittest.main()
