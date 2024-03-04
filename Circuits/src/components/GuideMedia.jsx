'use client';
import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {useLocation} from '@docusaurus/router';

export default function GuideMedia({fileName, fileType, width, height, useURL}) {
    let Width = typeof(width == String) ? width : "100%"
    let Height = typeof(height == String) ? height : "100%"

    fileType = fileType.toLowerCase()
    let CurrPage = useLocation().pathname.split("/")
    let lastElement = CurrPage.pop()

    if (lastElement == "") {
        lastElement = CurrPage.pop()
    }

    let fileURL = null

    if (useURL) {
        fileURL = fileName
    } else {
        fileURL = useBaseUrl(`/guides/${lastElement}/${fileName}`)
    }

    let returnValue = (<p>ERR: Asset not found</p>)
    switch (fileType) {
        case "image":
            returnValue = (<img src={fileURL} width={Width} height={Height}/>)
            break;
        case "video":
            returnValue = (<video src={fileURL} width={Width} height={Height} controls={true}/>)
            break;
        case "audio":
            returnValue = (
            <audio controls>
                <source src={fileURL} width={Width} height={Height} controls={true}/>
            </audio>)
            break;
        default:
            break;
    }

    return (<><div>{returnValue}</div></>)
}