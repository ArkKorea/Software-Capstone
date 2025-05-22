import flet as ft

def group_register_screen(page: ft.Page):
    def go_back(e):
        page.go("/myproductgroup")

    # 파일 선택기 객체
    file_picker = ft.FilePicker()

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            picked_file_text.value = f"선택한 파일: {e.files[0].name}"
            image_error_text.visible = False
        else:
            picked_file_text.value = "파일이 선택되지 않았습니다."
        page.update()

    file_picker.on_result = on_file_picked
    picked_file_text = ft.Text("", size=12)
    page.overlay.append(file_picker)

    # 검색창 초기화 함수
    def clear_search(e):
        search_field.value = ""
        search_field.update()

    search_field = ft.TextField(
        hint_text="상품명 검색",
        prefix_icon=ft.Icons.SEARCH,
        suffix_icon=ft.IconButton(icon=ft.Icons.CLOSE, on_click=clear_search),
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 10, 10, 10),
    )

    # 유효성 체크용 상태 변수
    group_name_field = ft.TextField(
        hint_text="제품명",
        border_color=ft.Colors.TRANSPARENT,
        border_radius=10,
        filled=True,
        fill_color=ft.Colors.GREY_100
    )
    group_name_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)

    # 상품 선택 (checkbox 상태 저장용 리스트)
    product_checkboxes = [ft.Checkbox(value=False) for _ in range(5)]
    product_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)

    # 대표 이미지 오류 표시
    image_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)

    # 저장 버튼 클릭 시 유효성 검사
    def save_clicked(e):
        has_error = False

        # 그룹명 확인
        if not group_name_field.value.strip():
            group_name_error_text.visible = True
            has_error = True
        else:
            group_name_error_text.visible = False

        # 상품 선택 확인
        if not any(cb.value for cb in product_checkboxes):
            product_error_text.visible = True
            has_error = True
        else:
            product_error_text.visible = False

        # 이미지 선택 확인
        if picked_file_text.value == "" or picked_file_text.value.startswith("파일이 선택되지"):
            image_error_text.visible = True
            has_error = True
        else:
            image_error_text.visible = False

        page.update()

        if not has_error:
            print("저장 완료!")  # 여기에 저장 로직 삽입
            page.go("/groupregistersuccess")

    return ft.View(
        "/groupregister",
        controls=[
            ft.AppBar(
                title=ft.Text("그 룹   추 가", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back
                ),
                actions=[
                    ft.Container(
                        margin=ft.Margin(0, 0, 10, 0),
                        content=ft.TextButton(
                            "저장",
                            on_click=save_clicked,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                        )
                    )
                ]
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding(left=20, right=20, top=10, bottom=20),
                content=ft.Column(
                    controls=[
                        # STEP 1
                        ft.Row(
                            controls=[
                                ft.Text("STEP 1", size=19, color=ft.Colors.GREEN),
                                ft.Text("  그룹명 입력", size=19, color=ft.Colors.BLACK)
                            ]
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=10,
                            padding=ft.Padding(10, 14, 10, 14),
                            margin=ft.Margin(0, 5, 0, 5),
                            content=group_name_field
                        ),
                        group_name_error_text,

                        # STEP 2
                        ft.Row(
                            controls=[
                                ft.Text("STEP 2", size=19, color=ft.Colors.GREEN),
                                ft.Text("  상품 선택", size=19, color=ft.Colors.BLACK)
                            ]
                        ),
                        ft.Container(
                            margin=ft.Margin(0, 5, 0, 0),
                            padding=ft.Padding(10, 10, 10, 10),
                            border=ft.Border(
                                top=ft.BorderSide(2, ft.Colors.GREEN),
                                right=ft.BorderSide(2, ft.Colors.GREEN),
                                bottom=ft.BorderSide(2, ft.Colors.GREEN),
                                left=ft.BorderSide(2, ft.Colors.GREEN)
                            ),
                            border_radius=10,
                            content=ft.Column(
                                controls=[
                                    search_field,
                                    *[
                                        ft.ListTile(
                                            leading=ft.CircleAvatar(
                                                content=ft.Text("A"),
                                                bgcolor=ft.Colors.GREEN
                                            ),
                                            title=ft.Text(f"내 상품 이름 {i+1}"),
                                            trailing=product_checkboxes[i]
                                        )
                                        for i in range(5)
                                    ]
                                ]
                            )
                        ),
                        product_error_text,

                        # STEP 3
                        ft.Container(
                            margin=ft.Margin(0, 20, 0, 10),
                            content=ft.Row(
                                controls=[
                                    ft.Text("STEP 3", size=19, color=ft.Colors.GREEN),
                                    ft.Text("  대표 이미지 업로드", size=19, color=ft.Colors.BLACK)
                                ]
                            )
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.ElevatedButton(
                                    "파일 선택",
                                    icon=ft.Icons.UPLOAD_FILE,
                                    on_click=pick_file
                                )
                                ,
                                picked_file_text
                            ]
                        ),
                        image_error_text
                    ],
                    scroll=ft.ScrollMode.HIDDEN
                )
            )
        ]
    )
