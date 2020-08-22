
def SSFP(self):
    self.flip_angle =int(self.ui.FA_Edit.text())
    row =self.size_image
    col =self.size_image
    theta = np.radians(self.flip_angle)
    TE =int(self.ui.TE_Edit.text())
    TR =int(self.ui.TR_Edit.text())
    Kspace_ssfp = np.zeros((self.img_array.shape[0] ,self.img_array.shape[1]) ,dtype=np.complex_)
    phantom = self.phantom(row ,col)

    phantom =self.startup_cycle(phantom ,theta /2 ,TE ,TR ,self.T2 ,self.T1 ,row ,col ,15)
    phantom =self.rotate_decay(phantom ,theta /2 ,TE ,self.T2 ,row ,col)
    phantom =self.startup_cycle(phantom ,theta ,TE ,TR ,self.T2 ,self.T1 ,row ,col ,15)

    for r in range(Kspace_ssfp.shape[0]):  # rows
        phantom =self.rotate_decay(phantom ,theta ,TE ,self.T2 ,row ,col)
        for c in range(Kspace_ssfp.shape[1]):
            Gx_step =(( 2 *math.pi ) /row ) *r
            Gy_step =(self.Gy /col ) *c
            for ph_row in range(row):
                for ph_col in range(col):
                    Toltal_theta =(Gx_step *ph_row ) +(Gy_step *ph_col)
                    Mag = math.sqrt(((phantom[ph_row ,ph_col ,0] ) *(phantom[ph_row ,ph_col ,0]) ) +
                                ((phantom[ph_row ,ph_col ,1] ) *(phantom[ph_row ,ph_col ,1])))

                    Kspace_ssfp[r ,c ] =Kspace_ssfp[r ,c ] +(Mag *np.exp(-1 j *Toltal_theta))
                    QApplication.processEvents()

            QApplication.processEvents()
        theta =-theta
        print(theta)
        for ph_rowtr in range(row):
            for ph_coltr in range(col):
                phantom[ph_rowtr ,ph_coltr ,2 ] =((phantom[ph_rowtr ,ph_coltr ,2] ) *np.exp
                    (-TR /self.T1[ph_rowtr ,ph_coltr]) ) +( 1 -np.exp(-TR /self.T1[ph_rowtr ,ph_coltr]))

        QApplication.processEvents()
    iff= np.fft.ifft2(Kspace_ssfp)

    # print(iff)
    inverse_array =np.abs(iff)
    inverse_array = (inverse_array - np.amin(inverse_array)) * 25 5/ (np.amax(inverse_array) - np.amin(inverse_array))
    inverse_img =gray2qimage(inverse_array)
    imgreconstruction = QPixmap(inverse_img  )  # piexel of image
    self.viewer2.setPhoto(QPixmap(imgreconstruction))

    def RF_rotate(self, theta, phantom, row, col):
        for i in range(row):
            for j in range(col):
                phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])

        return phantom

    def rotate(self, theta, phantom):
        RF = ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
        phantom = np.dot(RF, phantom)
        return phantom

    def decay(self, phantom, TE, T2):
        dec = np.exp(-TE / T2)
        phantom = np.dot(dec, phantom)
        return phantom

    def rotate_decay(self, phantom, theta, TE, T2, row, col):
        for i in range(row):
            for j in range(col):
                phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])
                phantom[i, j, :] = self.decay(phantom[i, j, :], TE, T2[i, j])
        return phantom

    def recovery(self, phantom, row, col, TR, T1):
        for ph_rowtr in range(row):
            for ph_coltr in range(col):
                phantom[ph_rowtr, ph_coltr, 0] = 0
                phantom[ph_rowtr, ph_coltr, 1] = 0
                phantom[ph_rowtr, ph_coltr, 2] = ((phantom[ph_rowtr, ph_coltr, 2]) * np.exp(
                    -TR / T1[ph_rowtr, ph_coltr])) + (1 - np.exp(-TR / T1[ph_rowtr, ph_coltr]))
        return phantom

           """
           for kr in range(row):
               for kc in range(col):
                   result = 0
                   for r in range(row):
                       for c in range(col):
                           Gx = ((2 * math.pi) / row) * r  # Frequency encodind
                           Gy = ((2 * math.pi) / col) * c  # Phase encodind
                           result = phantom[r, c] * np.exp(-1j * (Gy * kr + Gx * kc)) + result
                           QApplication.processEvents()

                   kspace[kr, kc] = result
           kspace = np.around(kspace)  # because of very small fractions

           return kspace
   
   
   
           """

