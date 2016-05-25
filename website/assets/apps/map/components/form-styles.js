const formStyles = {
  cursor: 'pointer',
  padding: 2,
  borderRadius: 0,
}

const bordered = {
  border: '1px solid #556377'
}

const inputStyle = {
  base: Object.assign({}, formStyles, {
    borderTop: 'none',
    borderLeft: 'none',
    borderBottom: '1px solid #af0623',
    borderRight: 'none',
  })
};

const labelStyle = {
  base: {
    span: {
      paddingRight: 6
    }
  }
}

const buttonStyle = {
  base: Object.assign({}, formStyles, bordered)
};

const selectStyle = {
  base: Object.assign({}, formStyles, bordered)
};

export {inputStyle, labelStyle, buttonStyle, selectStyle};