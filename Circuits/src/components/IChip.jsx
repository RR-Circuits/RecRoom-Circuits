'use client';
import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function IChip({uuid, redirect}) {
    let returnVal = <p>how in the world</p>
    const trueImage = <img src={useBaseUrl(`/img/chip/${uuid}.svg`)} />
    if (redirect) {
        returnVal = <a href={useBaseUrl(`/docs/chips/${uuid}`)}>{trueImage}</a>
    } else {
        returnVal = <img src={useBaseUrl(`/img/chip/${uuid}.svg`)} />
    }
    return (<><div>{returnVal}</div></>)
}