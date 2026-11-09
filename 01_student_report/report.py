from classroom import Classroom


def build_report(classroom: Classroom) -> str:
    # TODO: READMEの表示形式でレポートを作り、文字列として返す。
    lines = [
        classroom.name,
        f"学生数: {len(classroom.students)}"
    ]
    for student in classroom.students:
        if not student.scores:
            lines.append(f"{student.name}: 未受験")
            continue

        average = student.average()
        result = "合格○" if average >= 60 else "不合格×"
        lines.append(f"{student.name}: 平均{average:.1f}点 / {result}")

    return "\n".join(lines)