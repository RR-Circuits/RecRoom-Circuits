import React from 'react';

export default function IChip({uuid}) {
    return (<img src={require("@site/static/img/chip/" + uuid + ".svg")}></img>)
}