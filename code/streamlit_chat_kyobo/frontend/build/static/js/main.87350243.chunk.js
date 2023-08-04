(this.webpackJsonpstreamlit_component_template = this.webpackJsonpstreamlit_component_template || []).push([
    [0], {
        153: function(e, t, a) {
            e.exports = a(208)
        },
        208: function(e, t, a) {
            "use strict";
            a.r(t);
            var r, n, i = a(10),
                c = a.n(i),
                o = a(99),
                l = a.n(o),
                s = a(7),
                d = a(81),
                p = a(0),
                m = a(1),
                u = a(2),
                b = a(3),
                g = a(68),
                h = a(69),
                f = a(50),
                v = a(244),
                x = a(145),
                j = a(147),
                O = a(146),
                w = a(144),
                y = a(247),
                E = (a(161), a(162), function(e) {
                    Object(u.a)(a, e);
                    var t = Object(b.a)(a);

                    function a() {
                        var e;
                        Object(m.a)(this, a);
                        for (var i = arguments.length, o = new Array(i), l = 0; l < i; l++) o[l] = arguments[l];
                        return (e = t.call.apply(t, [this].concat(o))).render = function() {
                            g.a.setFrameHeight(window.innerHeight);
                            var t = e.props.args,
                                a = t.isUser,
                                i = t.avatarStyle,
                                o = t.seed,
                                l = t.message,
                                p = t.allow_html,
                                m = t.is_table,
                                u = "logo_".concat(a).concat(".png"),
                                b = e.props.theme;
                            
                            var chat_bg_color;
                            var chat_border;
                            if (a == true){
                                chat_bg_color = "rgb(225, 225, 225)"
                                chat_border = "2px solid rgb(180,180,180)"
                            }
                            else{
                                chat_bg_color = "rgb(240, 255, 240)"
                                chat_border = "2px solid rgb(144,238,144)"
                            }

                            if (!b) return c.a.createElement("div", null, "Theme is undefined, please check streamlit version.");
                            var E = h.a.img({
                                    border: "1px solid transparent",
                                    borderRadius: "50%",
                                    height: "3rem",
                                    width: "3rem",
                        
                                    margin: 0
                                }),
                                k = h.a.div({
                                    display: "inline-block",
                                    background: chat_bg_color,
                                    border: chat_border,
                                    borderRadius: "10px",
                                    padding: "5px 5px",
                                    margin: "5px 20px",
                                    maxWidth: "70%",
                                    fontSize:"12px",
                                    //whiteSpace: m ? "normal" : "pre-line"
                                    
                                }),
                                _ = h.a.div({
                                    display: "flex",
                                    fontFamily: "Segoe UI",
                                    color:"#000",
                                    height: "auto",
                                    fontSize:"20px",
                                    margin: 0,
                    
                                    width: "100%"
                                }, (function(e) {
                                    return e.isUser ? Object(f.a)(r || (r = Object(d.a)(["\n          flex-direction: row-reverse;\n          & > div {\n            text-align: right;\n          }        "]))) : Object(f.a)(n || (n = Object(d.a)([""])))
                                })),
                                S = [x.a, w.a],
                                U = [j.a].concat(Object(s.a)(p ? [O.a] : []));
                            return c.a.createElement(_, {
                                isUser: a
                            }, c.a.createElement(E, {
                                src: u,
                                alt: "profile",
                                draggable: "false"
                            }), c.a.createElement(k, null, c.a.createElement(v.a, {
                                remarkPlugins: S,
                                rehypePlugins: [].concat(Object(s.a)(U), [
                                    [y.a, {
                                        detect: !0,
                                        ignoreMissing:true
                                    }]
                                ])
                            }, l)))
                        }, e
                    }
                    return Object(p.a)(a)
                }(g.b)),
                k = Object(g.c)(E);
            l.a.render(c.a.createElement(c.a.StrictMode, null, c.a.createElement(k, null)), document.getElementById("root"))
        }
    },
    [
        [153, 1, 2]
    ]
]);
//# sourceMappingURL=main.87350243.chunk.js.map