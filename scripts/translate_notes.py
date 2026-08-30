except Exception as exc:
            error(f"{target.upper()} translation failed: {exc}")
            success = False

    # ======== 从这里开始替换 ========
    if translation_passed["en"] and translation_passed["fr"]:
        file_cache[relative] = current_md5
        save_cache(file_cache)  # 【关键新增】：每成功翻译完一篇，立刻保存到硬盘！
        info(f"  Cache updated and saved to disk for {relative}")

    return success, file_cache
    # ======== 替换到这里结束 ========


def verify_all_translations(files):
    info("")
    info("Verifying all translations...")
