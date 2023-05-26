import React from 'react';

export default function Highlight({targ}) {
    const downloadFile = () => {
        window.location.href = targ
    }
      
    const DownloadButton = <button onClick={downloadFile} />
  return (
    DownloadButton
  );
}