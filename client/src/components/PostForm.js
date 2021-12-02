import React, { useState } from "react";

function PostForm() {
  return (
    <div>
      <form action="#" method="post">
        <p>Name:</p>
        <input name="nm" type="text"></input>
        <input type="submit" value="submit"></input>
      </form>
    </div>
  );
}

export default PostForm;
