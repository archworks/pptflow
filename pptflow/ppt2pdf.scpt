--convert ppt to pdf
--参考1 https://github.com/jeongwhanchoi/convert-ppt-to-pdf
--参考2 https://www.polarzone.me/posts/random-snippets/ppt_to_pdf_batch_conversion/
--调用方式：osascript ppt2pdf.scpt {pptPath} {pdfPath} 参数需要为绝对路径
on run {pptPath, pdfPath}
    --set pdfPath to my makePdfPath(pptPath) --for debug
    tell application "Microsoft PowerPoint"
        --activate --for debug
        open pptPath 
        --save active presentation as (save as PDF) in POSIX file pdfPath --it's also ok
        save active presentation in (POSIX file pdfPath) as save as PDF
        close active presentation saving no
        quit
    end tell
end run

on makePdfPath(pptPath)
    if pptPath ends with ".pptx" then
        return (POSIX path of (text 1 thru -6 of pptPath)) & ".pdf"
    else
        return (POSIX path of (text 1 thru -5 of pptPath)) & ".pdf"
    end if
end makePdfPath