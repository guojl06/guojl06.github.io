import rhinoscriptsyntax as rs
import math

def create_3d_printable_falcon():
    rs.EnableRedraw(False)
    rs.Command("_SelAll")
    rs.Command("_Delete")

    # --- 1. 精准平面路径 ---
    segments = [
        [[257.1, 369.9], [195.5, 401.1], [186.3, 481.1], [240.7, 513.1]],
        [[240.7, 513.1], [273.7, 532.5], [311.7, 516.4], [324.0, 565.1]],
        [[324.0, 565.1], [289.0, 515.1], [231.0, 516.2], [199.1, 469.3]],
        [[199.1, 469.3], [201.3, 590.0], [303.9, 558.7], [303.0, 605.5]],
        [[303.0, 605.5], [282.2, 583.9], [247.3, 587.8], [220.3, 566.8]],
        [[220.3, 566.8], [242.5, 598.6], [260.1, 618.6], [305.1, 630.0]],
        [[305.1, 630.0], [330.8, 618.6], [366.4, 600.4], [370.7, 569.7]],
        [[370.7, 569.7], [373.8, 547.5], [365.3, 525.6], [340.9, 508.2]],
        [[340.9, 508.2], [374.9, 512.7], [394.3, 542.6], [385.5, 572.3]],
        [[385.5, 572.3], [424.1, 526.0], [390.8, 481.0], [327.1, 473.1]],
        [[327.1, 473.1], [379.8, 471.3], [417.6, 488.6], [407.8, 533.7]],
        [[407.8, 533.7], [427.6, 476.7], [407.9, 470.5], [377.2, 458.7]],
        [[377.2, 458.7], [369.3, 455.6], [362.6, 452.9], [356.8, 446.5]],
        [[356.8, 446.5], [339.8, 427.5], [354.1, 392.6], [384.3, 410.2]],
        [[384.3, 410.2], [385.6, 391.6], [379.0, 386.3], [358.1, 386.2]],
        [[358.1, 386.2], [319.5, 370.8], [294.4, 387.5], [275.3, 436.9]],
        [[275.3, 436.9], [288.6, 460.8], [253.1, 441.7], [253.7, 415.0]],
        [[253.7, 415.0], [286.7, 369.8], [243.3, 387.5], [218.2, 438.9]],
        [[218.2, 438.9], [258.9, 477.8], [214.3, 460.1], [220.0, 413.0]],
        [[220.0, 413.0], [257.1, 369.9], [257.1, 369.9], [257.1, 369.9]]
    ]

    all_crvs = []
    for seg in segments:
        pts = [[p[0], -p[1], 0] for p in seg]
        all_crvs.append(rs.AddNurbsCurve(pts, [0,0,0,1,1,1], 3))

    full_path = rs.JoinCurves(all_crvs, delete_input=True)[0]
    rs.CloseCurve(full_path)

    # --- 2. 打印友好型螺旋参数 ---
    # 降低总高度，减小坡度
    total_climb = 120.0 
    samples = 600
    path_domain = rs.CurveDomain(full_path)
    spiral_pts = []

    for i in range(samples + 1):
        u = float(i)/samples
        p = rs.EvaluateCurve(full_path, path_domain[0] + (path_domain[1] - path_domain[0]) * u)
        
        # 优化：前 5% 的路程 Z 轴保持在 0，形成稳固底座
        if u < 0.05:
            z_val = 0
        else:
            # 剩下的 95% 平滑上升
            z_val = ((u - 0.05) / 0.95) * total_climb
            
        spiral_pts.append([p[0], p[1], z_val])

    final_path = rs.AddInterpCurve(spiral_pts)
    rs.DeleteObject(full_path)

    # --- 3. 打印友好型截面 ---
    width = 16.0       # 稍宽一点增加结构强度
    thickness = 5.0    # 显著加厚，适合 FDM 堆叠
    domain = rs.CurveDomain(final_path)
    
    vertices = []
    face_indices = []

    for i in range(samples + 1):
        u = float(i) / samples
        t = domain[0] + (domain[1] - domain[0]) * u
        pt = rs.EvaluateCurve(final_path, t)
        tangent = rs.CurveTangent(final_path, t)
        
        side_vec = rs.VectorUnitize(rs.VectorCrossProduct(tangent, [0,0,1]))
        
        # 长方形截面，厚度增加。
        # 打印建议：将模型在切片软件里稍微倾斜，或使用 0.2mm 层高
        local_pts = [
            [-width/2, 0], 
            [width/2, 0], 
            [width/2, thickness], 
            [-width/2, thickness]
        ]
        
        for lp in local_pts:
            vx = pt[0] + lp[0] * side_vec[0]
            vy = pt[1] + lp[0] * side_vec[1]
            vz = pt[2] + lp[1]
            vertices.append([vx, vy, vz])

    # 4. Mesh 生成
    for i in range(samples):
        for j in range(4):
            face_indices.append([i*4+j, i*4+(j+1)%4, (i+1)*4+(j+1)%4, (i+1)*4+j])

    mesh = rs.AddMesh(vertices, face_indices)
    if mesh:
        rs.ObjectColor(mesh, [0, 194, 101])
        # 封口处理：3D 打印需要闭合实体 (Manifold)
        rs.Command("_FillMeshHoles")
        rs.UnifyMeshNormals(mesh)
    
    rs.DeleteObject(final_path)
    rs.ZoomExtents()
    rs.EnableRedraw(True)
    print("SUCCESS: 3D打印优化版完成。坡度已放缓，基座已加固。")

if __name__ == "__main__":
    create_3d_printable_falcon()