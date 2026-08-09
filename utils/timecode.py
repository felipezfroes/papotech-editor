def formatar_ms(
        ms
):

    total_segundos = int(
        ms / 1000
    )

    horas = (
        total_segundos // 3600
    )

    minutos = (
        total_segundos % 3600
    ) // 60

    segundos = (
        total_segundos % 60
    )

    return (
        f"{horas:02d}:"
        f"{minutos:02d}:"
        f"{segundos:02d}"
    )


def formatar_segundos(
        segundos
):

    return formatar_ms(
        segundos * 1000
    )


def formatar_srt(
        segundos
):

    ms_total = int(
        segundos * 1000
    )

    horas = (
        ms_total // 3_600_000
    )

    minutos = (
        ms_total % 3_600_000
    ) // 60_000

    secs = (
        ms_total % 60_000
    ) // 1000

    ms = (
        ms_total % 1000
    )

    return (
        f"{horas:02d}:"
        f"{minutos:02d}:"
        f"{secs:02d},"
        f"{ms:03d}"
    )