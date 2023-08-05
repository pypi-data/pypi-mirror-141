var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
import { isObject, isArray } from "./types";
import { BYTE_ORDER } from "./platform";
import { equals } from "./eq";
import { serialize } from "../serialization";
const __ndarray__ = Symbol("__ndarray__");
function encode_NDArray(array, serializer) {
    const encoded = serializer.encode(array.dtype == "object" ? Array.from(array) : array.buffer);
    return {
        type: "ndarray",
        array: encoded,
        order: BYTE_ORDER,
        dtype: array.dtype,
        shape: array.shape,
    };
}
export class BoolNDArray extends Uint8Array {
    constructor(seq, shape) {
        super(seq);
        this[_a] = true;
        this.dtype = "bool";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_a = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
BoolNDArray.__name__ = "BoolNDArray";
export class Uint8NDArray extends Uint8Array {
    constructor(seq, shape) {
        super(seq);
        this[_b] = true;
        this.dtype = "uint8";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_b = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Uint8NDArray.__name__ = "Uint8NDArray";
export class Int8NDArray extends Int8Array {
    constructor(seq, shape) {
        super(seq);
        this[_c] = true;
        this.dtype = "int8";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_c = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Int8NDArray.__name__ = "Int8NDArray";
export class Uint16NDArray extends Uint16Array {
    constructor(seq, shape) {
        super(seq);
        this[_d] = true;
        this.dtype = "uint16";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_d = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Uint16NDArray.__name__ = "Uint16NDArray";
export class Int16NDArray extends Int16Array {
    constructor(seq, shape) {
        super(seq);
        this[_e] = true;
        this.dtype = "int16";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_e = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Int16NDArray.__name__ = "Int16NDArray";
export class Uint32NDArray extends Uint32Array {
    constructor(seq, shape) {
        super(seq);
        this[_f] = true;
        this.dtype = "uint32";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_f = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Uint32NDArray.__name__ = "Uint32NDArray";
export class Int32NDArray extends Int32Array {
    constructor(seq, shape) {
        super(seq);
        this[_g] = true;
        this.dtype = "int32";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_g = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Int32NDArray.__name__ = "Int32NDArray";
export class Float32NDArray extends Float32Array {
    constructor(seq, shape) {
        super(seq);
        this[_h] = true;
        this.dtype = "float32";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_h = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Float32NDArray.__name__ = "Float32NDArray";
export class Float64NDArray extends Float64Array {
    constructor(seq, shape) {
        super(seq);
        this[_j] = true;
        this.dtype = "float64";
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_j = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
Float64NDArray.__name__ = "Float64NDArray";
export class ObjectNDArray extends Array {
    constructor(seq /* | ArrayBufferLike*/, shape) {
        /* TODO: TS 4.6
        if (seq instanceof ArrayBuffer) {
          throw new Error("not supported with dtype='object'")
        }
        */
        super(seq.length);
        this[_k] = true;
        this.dtype = "object";
        for (let i = 0; i < seq.length; i++) {
            this[i] = seq[i];
        }
        this.shape = shape ?? (is_NDArray(seq) ? seq.shape : [this.length]);
        this.dimension = this.shape.length;
    }
    [(_k = __ndarray__, equals)](that, cmp) {
        return cmp.eq(this.shape, that.shape) && cmp.arrays(this, that);
    }
    [serialize](serializer) {
        return encode_NDArray(this, serializer);
    }
}
ObjectNDArray.__name__ = "ObjectNDArray";
export function is_NDArray(v) {
    return isObject(v) && __ndarray__ in v;
}
export function ndarray(array, options = {}) {
    let { dtype } = options;
    if (dtype == null) {
        if (array instanceof ArrayBuffer || isArray(array)) {
            dtype = "float64";
        }
        else {
            dtype = (() => {
                switch (true) {
                    case array instanceof Uint8Array: return "uint8";
                    case array instanceof Int8Array: return "int8";
                    case array instanceof Uint16Array: return "uint16";
                    case array instanceof Int16Array: return "int16";
                    case array instanceof Uint32Array: return "uint32";
                    case array instanceof Int32Array: return "int32";
                    case array instanceof Float32Array: return "float32";
                    case array instanceof Float64Array: return "float64";
                    default: return "object";
                }
            })();
        }
    }
    const { shape } = options;
    switch (dtype) {
        case "bool": return new BoolNDArray(array, shape);
        case "uint8": return new Uint8NDArray(array, shape);
        case "int8": return new Int8NDArray(array, shape);
        case "uint16": return new Uint16NDArray(array, shape);
        case "int16": return new Int16NDArray(array, shape);
        case "uint32": return new Uint32NDArray(array, shape);
        case "int32": return new Int32NDArray(array, shape);
        case "float32": return new Float32NDArray(array, shape);
        case "float64": return new Float64NDArray(array, shape);
        default: return new ObjectNDArray(array, shape); // TODO: TS 4.6
    }
}
//# sourceMappingURL=ndarray.js.map